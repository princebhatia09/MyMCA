const router  = require("express").Router()
const multer  = require("multer");
const path = require("path");
const csvtojson = require('csvtojson'); 
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

        csvtojson().fromFile(req.file.path).then(source=>{
            console.log(req.file.filename)
            for (var i=0;i<source.length;i++){
                console.log(source[i]["CIN"])
            }
        })
        
        res.render("hander")
    })

    // res.json({message:"Sent"})
})



module.exports = router
