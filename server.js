
const express = require('express')
const app = express();
const multer = require('multer')
const cmd = require('node-cmd')
const sleep = require('system-sleep');
const fs = require('fs')
const port = 3000;

app.set("view engine",'ejs')
app.use(express.static('public'))

app.get('/',function(req,res){
  res.render("index");
})
/*

//for web
app.post('/uploadimg',multer({dest:'tmpimage/'}).single('upfile'),function(req,res){
  console.log('filename :'+req.file.filename + " is uploaded");
  cmd.get(
    'python netmodels/noneSquare_singletest.py --testimg tmpimage/'+req.file.filename,
    function(err,data,stderr){
      if(err){
        console.log(err)
        res.send("error occured" + err)
      }else{
        console.log("coloring has been doned")
        res.render("result",{
          imgpath : "result/tmpimage/" + req.file.filename+".png"
        })
      }
  })
})
*/

// not python daemon
app.post('/uploadND',multer({dest:'tmpimage/'}).single('upfile'),function(req,res){
  console.log('filename :'+req.file.filename + " is uploaded");
  cmd.get(
    'python netmodels/noneSquare_singletest.py --testimg tmpimage/'+req.file.filename,
    function(err,data,stderr){
      if(err){
        console.log(err)
        res.send("error occured" + err)
      }else{
        console.log("coloring has been done")
        const filename = req.file.filename + ".png"
        const options = {
          root : __dirname + '/public/result/tmpimage/',
          dotfiles:'deny',
          headers:{
            'x-timestamp' : Date.now(),
            'x-sent' :true
          }
        }
        res.sendFile(filename,options,function(err){
          if(err){
            next(err);
          }else{
            console.log('Sent',filename);
          }
        })
      }
  })
})
app.post('/upload',multer({dest:'tmpimage/'}).single('upfile'),function(req,res){
  console.log('filename :'+req.file.filename + " is uploaded");
  var i = 0;
  var outputfilename = req.file.filename+".png";
  var flag = false;
  while(i < 60){
    if(flag) break;
    fs.readdir('./public/result', (err,files) => {
      files.forEach(file => {
        if ( outputfilename == file){
          console.log("coloring has been done")
          const filename = outputfilename
          const options = {
            root : __dirname + '/public/result/',
            dotfiles:'deny',
            headers:{
              'x-timestamp' : Date.now(),
              'x-sent' :true
            }
          }
          //파일 다운로드
          res.download(options.root+outputfilename,function(err){
            if(err){
              next(err);
            }else{
              console.log('Sent',filename)
            }
          })
          /*
          //웹브라우저로 띄우기
          res.sendFile(filename,options,function(err){
            if(err){
              next(err);
            }else{
              console.log('Sent',filename);
            }
          })
          */
          flag = true;
        }
      })
    })
    sleep(1000)
    i++
  }

})


//app.use(express.static(path.join(__dirname,'public')));
app.listen(port,function(req,res){
  console.log("Server Running on "+port);
})
