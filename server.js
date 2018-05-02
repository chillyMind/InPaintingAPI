const express = require('express')
const app = express();
const multer = require('multer')
const cmd = require('node-cmd')
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
app.post('/upload',multer({dest:'tmpimage/'}).single('upfile'),function(req,res){
  console.log('filename :'+req.file.filename + " is uploaded");
  cmd.get(
    'python netmodels/noneSquare_singletest.py --testimg tmpimage/'+req.file.filename,
    function(err,data,stderr){
      if(err){
        console.log(err)
        res.send("error occured" + err)
      }else{
        console.log("coloring has been doned")
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


//app.use(express.static(path.join(__dirname,'public')));
app.listen(port,function(req,res){
  console.log("Server Running on "+port);
})
