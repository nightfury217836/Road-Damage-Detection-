let useWebcam = false;
let outputMediaPath = "";

/* ============================= ELEMENTS ============================= */
const uploadTab = document.getElementById("uploadTab");
const liveTab = document.getElementById("liveTab");
const uploadSection = document.getElementById("uploadSection");
const liveSection = document.getElementById("liveSection");
const dropZone = document.getElementById("dropZone");
const mediaUpload = document.getElementById("mediaUpload");
const preview = document.getElementById("preview");
const webcam = document.getElementById("webcam");
const predictBtn = document.getElementById("predictBtn");
const loader = document.getElementById("loader");

/* ============================= TAB SWITCHING ============================= */
uploadTab.onclick = () => {
    useWebcam = false;
    uploadSection.classList.remove("hidden");
    liveSection.classList.add("hidden");
    uploadTab.classList.add("active");
    liveTab.classList.remove("active");
};

liveTab.onclick = () => {
    useWebcam = true;
    uploadSection.classList.add("hidden");
    liveSection.classList.remove("hidden");
    liveTab.classList.add("active");
    uploadTab.classList.remove("active");
    startWebcam();
};

/* ============================= FILE UPLOAD PREVIEW ============================= */
dropZone.onclick = () => mediaUpload.click();

mediaUpload.onchange = () => {
    handleMedia(mediaUpload.files[0]);
};

function handleMedia(file) {
    if (!file) return;

    const url = URL.createObjectURL(file);

    /* Replace dropzone content instead of hiding it */
    dropZone.innerHTML = "";

    if (file.type.startsWith("image")) {
        dropZone.innerHTML = `<img src="${url}">`;
    } else {
        dropZone.innerHTML = `<video src="${url}" controls></video>`;
    }
}


/* ============================= WEBCAM ============================= */
async function startWebcam() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcam.srcObject = stream;
}

/* ============================= PREDICT BUTTON ============================= */
predictBtn.onclick = async () => {

    loader.classList.remove("hidden");

    const formData = new FormData();


    if (!useWebcam) {

        const file = mediaUpload.files[0];

        if (!file) {
            alert("Upload file first");
            loader.classList.add("hidden");
            return;
        }

        /* Flask expects these keys */
        if (file.type.startsWith("image")) {

            formData.append("file", file);

            const res = await fetch("/predict_image", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            updateCounters(data.counts);
            showOutput(data.result_image);

        } else {

            formData.append("file", file);

            const res = await fetch("/predict_video", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            updateCounters(data.counts);
            showOutput(data.result_videoz);
        }

    } else {
        alert("Live prediction not connected to backend yet");
    }

    loader.classList.add("hidden");
};

/* ============================= UPDATE COUNTERS ============================= */
function updateCounters(c) {
    document.getElementById("D00").innerText = c.D00 || 0;
    document.getElementById("D10").innerText = c.D10 || 0;
    document.getElementById("D20").innerText = c.D20 || 0;
    document.getElementById("D40").innerText = c.D40 || 0;
    document.getElementById("OTHER").innerText = c.OTHER || 0;
}

/* ============================= SHOW OUTPUT MEDIA ============================= */
function showOutput(path) {

    // Save path for download
    outputMediaPath = path;

    dropZone.innerHTML = "";

    if (path.endsWith(".mp4")) {
        dropZone.innerHTML =
            `<video src="${path}" controls autoplay></video>`;
    } else {
        dropZone.innerHTML =
            `<img src="${path}">`;
    }
}



/* ============================= DOWNLOAD CSV REPORT ============================= */
const downloadBtn = document.getElementById("downloadBtn");

if (downloadBtn) {
    downloadBtn.addEventListener("click", () => {

        if (!outputMediaPath) {
            alert("No result to download");
            return;
        }

        const link = document.createElement("a");
        link.href = outputMediaPath;

        // Auto filename
        if (outputMediaPath.endsWith(".mp4")) {
            link.download = "annotated_result.mp4";
        } else {
            link.download = "annotated_result.jpg";
        }

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

