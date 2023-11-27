// Verificando se a API da câmera está disponível

(function () {
    if (!("mediaDevices" in navigator) || !("getUserMedia" in navigator.mediaDevices)) {
        alert("Camera API is not available in your browser");
        return;
    }

    // Obtendo os elementos da página
    const video = document.querySelector("#video");
    const btnPlay = document.querySelector("#btnPlay");
    const btnPause = document.querySelector("#btnPause");
    const btnScreenshot = document.querySelector("#btnScreenshot");
    const btnChangeCamera = document.querySelector("#btnChangeCamera");
    const screenshotsContainer = document.querySelector("#screenshots");
    const canvas = document.querySelector("#canvas");
    const devicesSelect = document.querySelector("#devicesSelect");

    // Configurando a câmera
    const constraints = {
        video: {
            width: {
                min: 1280,
                ideal: 1920,
                max: 2560,
            },
            height: {
                min: 720,
                ideal: 1080,
                max: 1440,
            },
        },
    };

    // Flag para a câmera frontal e traseira
    let useFrontCamera = true;

    // Stream de vídeo atual
    let videoStream;

    // Manipulação de eventos
    // Função para iniciar a reprodução do vídeo
    function playVideo() {
        video.play();
        btnPlay.classList.add("is-hidden");
        btnPause.classList.remove("is-hidden");
    }

    // Função para pausar o vídeo
    function pauseVideo() {
        video.pause();
        btnPause.classList.add("is-hidden");
        btnPlay.classList.remove("is-hidden");
    }

    // Adiciona ouvintes de eventos aos botões de play e pause
    btnPlay.addEventListener("click", playVideo);
    btnPause.addEventListener("click", pauseVideo);

    // Função para tirar uma captura de tela
    btnScreenshot.addEventListener("click", function () {
        const img = document.createElement("img");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        img.src = canvas.toDataURL("image/png");
        screenshotsContainer.prepend(img);
    // Chamando a função para salvar a foto    
        savePhoto(canvas.toDataURL("image/png"))
    });


    // Função para salvar a foto
    function savePhoto(dataURL) {
    // Cria um objeto de solicitação HTTP
    const xhr = new XMLHttpRequest();

    // Define o tipo de solicitação, a URL e se será assíncrono
    xhr.open("POST", "/save_photo", true);

    // Define o cabeçalho da solicitação
    xhr.setRequestHeader("Content-Type", "application/json");

    // O que fazer quando a resposta da solicitação estiver pronta
    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log("Photo saved successfully!");
        } else {
            console.error("Failed to save photo. Status: " + xhr.status);
        }
    };

    // O que fazer em caso de erro na solicitação
    xhr.onerror = function () {
        console.error("Error occurred during photo saving.");
    };

    // Envia a solicitação com os dados da foto
    xhr.send(JSON.stringify({ photoData: dataURL }));
}

    

    // Adiciona um ouvinte de evento ao botão de mudança de câmera
    btnChangeCamera.addEventListener("click", function () {
        useFrontCamera = !useFrontCamera;
        initializeCamera();
    });

    // Função para parar o stream de vídeo
    function stopVideoStream() {
        if (videoStream) {
            videoStream.getTracks().forEach((track) => {
                track.stop();
            });
        }
    }

    // Inicialização da câmera
    async function initializeCamera() {
        stopVideoStream();
        constraints.video.facingMode = useFrontCamera ? "user" : "environment";

        try {
            // Obtém o stream de vídeo da câmera
            videoStream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = videoStream;
            playVideo(); // Inicia automaticamente a reprodução ao trocar de câmera
        } catch (err) {
            alert("Could not access the camera");
        }
    }

    initializeCamera();

})();
