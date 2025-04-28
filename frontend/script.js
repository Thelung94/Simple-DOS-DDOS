async function startRequests() {
    const url = document.getElementById('url').value;
    const total = document.getElementById('total_requests').value;

    if (!url || !total) {
        alert("Please enter URL and total requests.");
        return;
    }

    document.getElementById('status').innerText = "Start Attack...";
    await eel.start_requests(url, total)();
}

eel.expose(update_status);
function update_status(success, fail) {
    const total = parseInt(document.getElementById('total_requests').value) || 1; // avoid divide by zero
    const completed = success + fail;
    const percent = Math.min(Math.round((completed / total) * 100), 100);

    document.getElementById('status').innerText = `Success: ${success} | Fail: ${fail}`;

    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = percent + "%";
    progressBar.innerText = percent + "%";
}

async function addProxy() {
    const proxyInput = document.getElementById('proxy_input');
    const proxyValue = proxyInput.value.trim();
    if (proxyValue) {
        await eel.add_proxy(proxyValue)();
        proxyInput.value = '';
        loadProxies();
    }
}

async function stopRequests() {
    await eel.stop_requests()();
    document.getElementById('status').innerText = "Stopping Attack...";
}


async function removeProxy(proxy_ip) {
    await eel.delete_proxy(proxy_ip)();
    loadProxies();
}

async function loadProxies() {
    const proxyListElement = document.getElementById('proxy_list');
    proxyListElement.innerHTML = '';

    const proxies = await eel.get_proxies()();
    console.log(proxies)
    proxies.forEach(proxy => {
        proxyListElement.innerHTML += `<li>${proxy} <button onclick="removeProxy('${proxy}')">Remove</button></li>`;
    });
}

// Load proxies on page load
window.onload = loadProxies;
