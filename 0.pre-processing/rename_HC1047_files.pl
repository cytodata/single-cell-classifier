#!/usr/bin/perl                                                                                                                                                                                                                                                                                                      
use strict;
use warnings;

use File::Find;

my $infolder=$ARGV[0];

while("on" eq "on"){
    opendir(my $bigindir, $infolder);
    print $infolder;
   
    foreach my $subfolder (sort readdir($bigindir)){
       
        if($subfolder=~m/2011/){
             print $subfolder."\n";
                                        find({wanted => sub {
                                        if(-d $_ && $_=~m/thumbs/){
                                            $File::Find::prune = 1;
                                            return;
                                    }
                                     #last;
                            #./cyto_data_challenge/2011-11-17_X-Man_LOPAC_X05_LP_S03_2/A - 19(fld 4 wv DAPI - DAPI).tif
                                    if($_=~m/wv/){
                                    if($_=~m/.*\/(.+\/.+)\)\.tif/){
                                        my $newname=$1;
                                        $newname=~s/\W/_/g;                                       
                                        $newname=~s/^_//g;                                       
                                        $newname=~s/fld/_/g;
                                        $newname=~s/wv/_/g;
                                        $newname=~s/0(\d)/$1/g;
                                        $newname=~s/_+/_/g;
                                        $newname=~s/([A-Z])_(\d+?)_/$1$2_/g;                                        
                                        $newname=~s/DAPI_DAPI/DAPI/g;
                                        $newname=~s/Cy3_Cy3/Cy3/g;
                                        $newname=~s/Cy5_Cy5/Cy5/g;
                                        $newname=~s/FITC_FITC/FITC/g;
                                        if($_=~m/(.*\/.+\/).+\)\.tif/){                                            
                                            my $dir=$1;
                                            rename($_,$dir."/$newname.tif");                                        
                                        }
                                }
                                    }
                                          },
                                      no_chdir => 1},$infolder."/".$subfolder);
        }
        
        print "done\n";

    }
}
