const router  = require("express").Router()
const multer  = require("multer");
const path = require("path");
const csvtojson = require('csvtojson'); 
// import {PythonShell} from "python-shell"
const {PythonShell} =  require("python-shell");
const fs = require("fs")
const csv  = require("csv-parser");
const spawn = require('child_process').spawn;

let storage = multer.diskStorage({

    destination: (req,file,cb)=> cb(null,"uploads/"),
    filename :(req,file,cb)=>{
        const uniquename = `${Date.now()}-${Math.round(Math.random() * 1E9)}${path.extname(file.originalname)}`;
        cb(null,uniquename);
    }
})

let upload = multer({

    storage,
    limit: {fileSize:1000000*100},

}).single('file');

router.get("/",(req,res)=>{
    res.render("hander")
})

router.post("/Postapi",(req,res)=>{

    upload(req,res,(err)=>{

        if (!req.file){
            return res.json({file:"Did you Upload FIle? Go back and upload File"})
        }
        if(err){
            return res.status(500).send({error:err.message});
        }
        fs.writeFileSync('./abc.txt', req.file.path);

        PythonShell.run('./pythonScripts/MCAGov.py', null, function (errs) {
            if (errs) throw errs;
            console.log(path.dirname(require.main.filename))      
            res.json({mainFile:"dataFileFolder/AN CIN LIST_DATA.csv",ErroFile:"dataFileFolder/ErrorGivenByWebsite.csv"})
          });

    })

    // res.json({message:"Sent"})
})

router.get("/:dir/:file",(req,res)=>{
    const dir = req.params.dir
    const file = req.params.file
    newPah = path.join(path.dirname(require.main.filename),"dataFileFolder") 
    res.sendFile(newPah+"/"+file)

})


module.exports = router