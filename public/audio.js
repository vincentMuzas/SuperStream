$( document ).ready(function() {
    
    var video = $("#my-video_html5_api");
    var videoObj = video.get(0);
    var audio = $("#audio_playback").get(0);
    video.on("play", function(){
        audio.play();
        audio.currentTime = videoObj.currentTime;
    })
    video.on("pause", function(){
        audio.pause();
    })
    video.on("volumechange", function(){
        audio.volume = videoObj.volume;
    })

    function syncTracks() {

        var Atime = audio.currentTime;
        var Vtime = videoObj.currentTime;
        if (Atime < Vtime - 0.2 || Atime > Vtime + 0.2) {
            audio.muted = 1
            audio.currentTime = videoObj.currentTime;
        }
        else {
            audio.muted = videoObj.muted;
        }
    }
    setInterval(syncTracks, 200);

    
});
function setAudio(obj) {
    let audio = $("#audio_playback")[0]
    audio.src = $(obj).attr("audioURL");
    audio.currentTime = $("#my-video_html5_api").get(0).currentTime;
    audio.muted = 1;
    audio.play();
}
