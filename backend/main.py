import eel
from . import db, requester
import asyncio
import aiohttp

status = {
    'success': 0,
    'fail': 0,
    'total': 0
}

stop_requested = False
active_tasks = []  # New: track active tasks

def start_backend():
    pass

@eel.expose
def add_proxy(proxy_ip):
    db.save_proxy(proxy_ip)

@eel.expose
def delete_proxy(proxy_ip):
    db.delete_proxy(proxy_ip)

@eel.expose
def start_requests(target_url, total_requests):
    global stop_requested, active_tasks
    stop_requested = False
    active_tasks = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(internal_start_requests(target_url, total_requests))

@eel.expose
def stop_requests():
    global stop_requested, active_tasks
    stop_requested = True

    for task in active_tasks:
        if not task.done():
            task.cancel()
    print("[*] Stop requested: cancelling active tasks...")

@eel.expose
def get_proxies():
    return db.get_all_proxies()

async def internal_start_requests(target_url, total_requests):
    proxy_list = db.get_all_proxies()
    total_requests = int(total_requests)
    status['success'] = 0
    status['fail'] = 0
    status['total'] = total_requests

    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        for i in range(total_requests):
            proxy = None
            if proxy_list:
                proxy = proxy_list[i % len(proxy_list)]

            task = asyncio.create_task(single_request_worker(session, target_url, proxy))
            active_tasks.append(task)

        try:
            await asyncio.gather(*active_tasks, return_exceptions=True)
        except asyncio.CancelledError:
            print("[!] Requests were cancelled.")

    # Save final result to database
    db.save_result(
        url=target_url,
        total_requests=total_requests,
        success=status['success'],
        fail=status['fail']
    )

async def single_request_worker(session, target_url, proxy):
    global stop_requested

    if stop_requested:
        return

    try:
        result = await requester.send_request(session, target_url, proxy)

        if result:
            status['success'] += 1
        else:
            status['fail'] += 1

        eel.update_status(status['success'], status['fail'])()
    except asyncio.CancelledError:
        # Handle if task is cancelled mid-request
        print("[!] Task was cancelled before finishing request.")
