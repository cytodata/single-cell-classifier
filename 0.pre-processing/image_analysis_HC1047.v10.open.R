#!/usr/bin/R
library(EBImage)
library(FNN)
library(geometry)
library(stringr)
library(e1071)
library(dplyr)
library(RPostgreSQL)
library(dbplyr)

test_db <- src_postgres(
  dbname = "example_db",
  host = "some_server",
  user = "user",
  password = "passwd"
)

analyze<-function(image_string){
  start.time <- Sys.time()
  images=unlist(strsplit(x=image_string,split="::")) 
  nuc_image_name = images[1] 
  body_image_name = images[2] 
  if(file.exists(nuc_image_name) && file.exists(body_image_name)){
    
    #badcells=c()
    
    identifier=sub(".*/(.+)_\\w+.tif","\\1",nuc_image_name,perl=TRUE);
    
    print(identifier)
    
    TEST_IMAGE_nuclei_raw=readImage(nuc_image_name)[400:1800,400:1800]#[500:1500,500:1500]
    if(min(TEST_IMAGE_nuclei_raw)==0){
      if(quantile(TEST_IMAGE_nuclei_raw,0.01)!=0){
        TEST_IMAGE_nuclei=gblur(normalize(log(TEST_IMAGE_nuclei_raw+quantile(TEST_IMAGE_nuclei_raw,0.01))),sigma=1)
      }else{
        TEST_IMAGE_nuclei=gblur(normalize(log(TEST_IMAGE_nuclei_raw+0.0000001)),sigma=1)
      }
    }else{
      TEST_IMAGE_nuclei=gblur(normalize(log(TEST_IMAGE_nuclei_raw)),sigma=1)  
    }
    
    TEST_IMAGE_actin_raw=readImage(body_image_name)[400:1800,400:1800]#[500:1500,500:1500]
    if(min(TEST_IMAGE_actin_raw)==0){
  	  if(quantile(TEST_IMAGE_actin_raw,0.01)!=0){
  		  TEST_IMAGE_actin=gblur(normalize(log(TEST_IMAGE_actin_raw+quantile(TEST_IMAGE_actin_raw,0.01))),sigma=1)
  		}else{
  		  TEST_IMAGE_actin=gblur(normalize(log(TEST_IMAGE_actin_raw+0.0000001)),sigma=1)
  		}
    }else{
      TEST_IMAGE_actin=gblur(normalize(log(TEST_IMAGE_actin_raw)),sigma=1)  
    }

    nuclei_objects = bwlabel(fillHull(opening(thresh(TEST_IMAGE_nuclei,w=31,h=31,offset=0.065))))      
    
    body_binary<-TEST_IMAGE_actin/TEST_IMAGE_actin
    
    body_binary[TEST_IMAGE_actin<0.25]<-0 #18
    body_binary=fillHull(opening( body_binary))
    
    cell_bodies_objects= propagate(TEST_IMAGE_actin, seeds= nuclei_objects, mask=body_binary,lambda=3e-4)
    
    if(max(nuclei_objects)>30){    
      DNA_features = computeFeatures(nuclei_objects, ref=TEST_IMAGE_nuclei_raw, 
                                     methods.noref=c("computeFeatures.shape"),
                                     methods.ref=c("computeFeatures.basic", "computeFeatures.moment", "computeFeatures.haralick"),
                                     xname="DNA", refnames="0", properties=FALSE, expandRef=NULL, 
                                     basic.quantiles=c(0.05,0.1,0.5), haralick.scales=c(1,2,3)
      )   
      colnames(DNA_features) = sub(".0.", ".", colnames(DNA_features))    
      
      
      rm(body_binary)
      actin_features = computeFeatures(cell_bodies_objects, ref=TEST_IMAGE_actin_raw, 
                                       methods.noref=c("computeFeatures.shape"),
                                       methods.ref=c("computeFeatures.basic", "computeFeatures.moment", "computeFeatures.haralick"),
                                       xname="actin", refnames="0", properties=FALSE, expandRef=NULL, 
                                       basic.quantiles=c(0.05,0.1,0.5), haralick.scales=c(1,2,3)
      )   
      colnames(actin_features) = sub(".0.", ".", colnames(actin_features))     
      
      nearest.neighbours = get.knn(actin_features[, c("actin.m.cx", "actin.m.cy")],k=30)[["nn.dist"]][,c(10,20,30)]
      colnames(nearest.neighbours) = c("dist.10.nn","dist.20.nn","dist.30.nn")
      
      nucleus.displacement = sqrt(rowSums((actin_features[,c("actin.m.cx", "actin.m.cy")] - DNA_features[,c("DNA.m.cx", "DNA.m.cy")])^2))
      names(nucleus.displacement) = c("nuclear.displacement")
      
      cell_features=cbind(
        actin_features,
        DNA_features,
        nearest.neighbours,
        nucleus.displacement
      )
      colnames(cell_features)=c(
        colnames(actin_features),
        colnames(DNA_features),
        colnames(nearest.neighbours),
        "nuclear.displacement"
      )
      
      barcodes=str_match(identifier,"(211_11_17_X_Man_LOPAC_X5_LP_(\\w+?)_(\\w+?)_(\\w+?)_(\\d+))")
      
      tmp=colnames(cell_features)
      tmpf=cell_features
      cell_features=
        cbind.data.frame(
          as.data.frame(matrix(barcodes[2:6],nrow=nrow(cell_features),ncol=length(barcodes[2:6]),byrow=TRUE)),
          cell_features
        )
      colnames(cell_features)=c("barcode","plate","replicate","well","field",tmp)
      
      cell_features<-cell_features[,-1]
      cell_features$well<-gsub(pattern = "([A-Z])(\\d)$",replacement ="\\10\\2" ,x = cell_features$well)
      cell_features$plate<-gsub(pattern = "([A-Z])(\\d)",replacement ="P\\2" ,x = cell_features$plate)
      
      img_raw = rgbImage(green=TEST_IMAGE_actin_raw , blue=TEST_IMAGE_nuclei_raw)
      
      single_cells<-stackObjects(x = cell_bodies_objects, ref = normalize(img_raw),ext = 100)
      
      subset<-sample(1:nrow(cell_features),size = 200)
     
      #save(cell_features,file=paste(dir,"/",identifier,"_single_cell.RData",sep=""))
      #copy_to(test_db, cell_features, name="D1086_single_cell", temporary = FALSE, indexes = list("plate","screen", "well","field"))
      #db_insert_into( con = test_db$con, table = "D1086_single_cell_V1", values = cell_features)
      dbWriteTable(test_db$con,"HC1047_single_cell_V1",cell_features[subset,],append=TRUE,row.names=FALSE)
      writeImage(single_cells,paste0(dir,"/",identifier,"_",1:nrow(cell_features[subset,]),".tiff"))
      
      img = rgbImage(green=TEST_IMAGE_actin , blue=TEST_IMAGE_nuclei)
      res = paintObjects(nuclei_objects, img, opac=c(0.8),thick=0.3, col='white')
      res = paintObjects(cell_bodies_objects, img, opac=c(0.8),thick=0.3, col='green')
      writeImage(res, file=paste(dir,"/",identifier,"_segmented",".png",sep=""), type="png", quality = 10, 8 )
    }
  }
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  print(time.taken)
}

args=commandArgs(trailingOnly = TRUE)
options("scipen"=100, "digits"=4,warn=-1,MulticoreParam=quote(MulticoreParam(workers=6)))
dir=args[length(args)];
args=as.list(args[-length(args)])
result=lapply(as.list(args),analyze)


