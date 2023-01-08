const { time } = require('console');
var express = require('express');
var router = express.Router();
var videoFolder = "./public/Videos/";

const fs = require('fs');

/* GET home page. */
router.get(['/', "/search"], function(req, res, next) {
  let fileArr = Array();
  let folderArr = Array();

  localPath = videoFolder + (req.query.path ? req.query.path + '/' : '')

  fs.readdirSync(localPath).forEach(file => {
    if (fs.lstatSync(localPath + file).isDirectory()) {
      folderArr.push({
        type: "folder",
        name: file,
        path: "/video/search?path=" + (req.query.path ? req.query.path + '/' : '') + file,
        subtitles: "",
        icon: "folder",
        icon_color: "green",
      });
    }
    else if (file.endsWith(".mp4"))
      fileArr.push({
        type: "file",
        name: file.slice(0, -4),
        path: "/video/watch?q=" + (req.query.path ? req.query.path + '/' : '') + file,
        icon: "play_arrow",
        icon_color: "red",
      });
  });

  res.render('video_index', { title: 'Vidéo', files: folderArr.concat(fileArr) });
});

router.get('/watch', function(req, res, next) {
  subtitles = Array();
  audio = Array();

  let url = req.query.q
  var to = url.lastIndexOf('/');
  to = to == -1 ? url.length : to + 1;
  localPath = "./public/Videos/" + url.substring(0, to);
  webpath = "/Videos/" + url.substring(0, to);
  filename = url.substring(to, url.length - 4);
  
  fs.readdirSync(localPath).forEach(file => {
    if (file.endsWith(".vtt") && file.startsWith(filename))
      subtitles.push({
        type: "file",
        name: file.substring(filename.length + 1, file.length - 4),
        srclang: 0,
        path: webpath + file
      }
    );
  });

  fs.readdirSync(localPath).forEach(file => {
    if (file.endsWith(".mp3") && file.startsWith(filename))
      audio.push({
        type: "file",
        name: file.substring(filename.length + 1, file.length - 4),
        path: webpath + file
      }
    );
  });

  res.render('video_watch.jade',
    {
      title: "Watch " + req.query.q.split('/').at(-1).slice(0, -4),
      videoURL: "/Videos/" + req.query.q,
      subtitles: subtitles,
      audio: audio
    });
})

module.exports = router;
