async function getData() {
    const response = await fetch("/?all");
    return response.json();
}


function createSpans() {
    let span_div_html = "";
    /* ids is defined in index.html */
    Object.entries(ids).forEach(([element_id, element]) => {
        let description = element_id.replace("_", " ");
        if (element.desc !== undefined) {
            description = element.desc;
        }
        if (element.type === "bool" || element.type === "action") {
            span_div_html += `<span class="pf_span off" id=${element_id} onclick="toggle('${element_id}')">${description}</span>`
        } else {
            width = TYPES[element.type][0];
            span_div_html += `<span class="pf_span">${description} <input id="${element_id}"  style="width: ${width}ch;"></span>`;
        }
    });
    span_div = document.getElementById("spans");
    span_div.innerHTML = span_div_html;

    // make enter press upload button
    span_div.addEventListener("keyup", event => {
        if (event.keyCode === 13) { // enter key
            event.preventDefault();
            uploadValues();
        }
    });
}


function isNumeric(num) {
    return (typeof(num) === 'number' || typeof(num) === "string" && num.trim() !== '') && !isNaN(num);
}


function refreshPage() {
    Object.entries(ids).forEach(([element_id, element]) => { //ids declared previous to this script in each page
        let docElement = document.getElementById(element_id);
        let value = element.val;
        if (isNumeric(value)) {
            value = parseFloat(value);
            if (element.type === "number") { // integer or float
                if (Math.floor(value) !== value) { //float
                    value = value.toFixed(2);
                }
            } else if (element.type === "date") {
                date = new Date(value * 1000); // js uses ms
                value = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;
            }
        } else if (element.type === "bool") {
            if (value == true || value === "true" || value === "True" || value === "ON") {
                value = "true";
            } else {
                value = "false";
            }
        }
        docElement.value = value; //TODO have some fields not changed by ids.val?
        element.val = value; // reset to refreshed version TODO check this is necessary?
        if (element.type === "bool") {
            docElement.className = (element.val ? "pf_span on" : "pf_span off");
        }
    });
}


function refreshData() {
    getData().then(ret_val => {
        let data_changed = false;
        Object.entries(ret_val).forEach(([key, val]) => {
            if (key in ids && ids[key].val != val) {
                data_changed = true;
                ids[key].val = val;
            }
        });
        if (data_changed) {
            refreshPage();
        }
    });
}


function repeatRefresh() {
    refreshData();
    refreshImage();
    setTimeout(repeatRefresh, 120000); //refresh every 120s in never-ending loop
}


function uploadValues() {
    let data_changed = false;
    Object.entries(ids).forEach(([element_id, element]) => { //ids declared previous to this script in each page
        if (element.fn === "setter" && element.type !== "bool") { // done by toggle function.
            let docElement = document.getElementById(element_id);
            if (docElement.value != element.val) {
                console.log("updating:" + element_id + "->" + docElement.value + ":was:" + element.val + ":");
                element.val = docElement.value;
                fetch(`/?${element_id}=${docElement.value}`).then(() => data_changed = true); //TODO do we need to refresh?
            }
        }
    });
    if (data_changed) { //TODO - is this necessary in ids.val changed here?
        refreshData();
    }
}


function toggle(id) {
    let element = ids[id];
    if (element.type === "bool") { //toggle val and class
        element.val = !(element.val);
    }
    let cmd = `/?${id}=${element.val}`
    if (element.fn !== "setter") { // i.e. use fn
        cmd = `/?${element.fn}`;
        cmd = cmd.replace('$val', element.val);
    }
    let docElement = document.getElementById(id);
    let css = (element.val ? "pf_span on" : "pf_span off"); // return to this
    docElement.className = "pf_span flash";
    console.log(cmd);
    fetch(cmd).then(() => afterFlash(docElement, css));
}


function afterFlash(element, css) {
    element.className = css; //TODO slight time delay?
}


// the super slimmed down python server doesn't load style sheets from file so this is
// done using javascript!
function setStyle() {
    var x = document.createElement("STYLE");
    var t = document.createTextNode("body {\
        background-color: #1a1a1a;\
        color: #e0e0e0;\
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;\
        line-height: 1.6;\
        margin: 0;\
        padding: 20px;\
    }\
    #current-image-container {\
        margin-top: 20px;\
        padding: 10px;\
        background-color: #2c3e50;\
        border-radius: 8px;\
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);\
        display: flex;\
        justify-content: center;\
        align-items: center;\
    }\
    #current-image {\
        max-width: 100%;\
        max-height: 400px;\
        object-fit: contain;\
        border-radius: 4px;\
    }\
    button {\
        margin: 8px;\
        padding: 12px 20px;\
        border: none;\
        border-radius: 6px;\
        font-weight: 600;\
        background-color: #2c3e50;\
        color: #ecf0f1;\
        cursor: pointer;\
        transition: all 0.2s ease;\
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);\
    }\
    button:hover {\
        background-color: #34495e;\
        transform: translateY(-1px);\
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);\
    }\
    .off {\
        background-color: #c0392b;\
        color: #ecf0f1;\
        transition: all 0.3s ease;\
    }\
    .on {\
        background-color: #27ae60;\
        color: #ecf0f1;\
        transition: all 0.3s ease;\
    }\
    .flash {\
        background-color: #f39c12;\
        color: #ecf0f1;\
        animation: flash 0.5s ease-in-out;\
    }\
    .pf_span {\
        margin: 4px;\
        padding: 8px 12px;\
        border-radius: 4px;\
        border: 1px solid rgba(255,255,255,0.1);\
        display: inline-block;\
        cursor: pointer;\
        transition: all 0.2s ease;\
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);\
    }\
    .pf_span:hover {\
        transform: translateY(-1px);\
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);\
    }\
    @keyframes flash {\
        0% { opacity: 1; }\
        50% { opacity: 0.7; }\
        100% { opacity: 1; }\
    }");
    x.appendChild(t);
    document.head.appendChild(x);
}

function refreshImage() {
    const image = document.getElementById('current-image');
    image.src = '/current_image?' + new Date().getTime(); // Add timestamp to prevent caching
}
