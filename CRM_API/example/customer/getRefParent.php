<?php
$url='http://amls.intrumnet.com:81/sharedapi/purchaser/filter';  
$params=array(     
            'fields' => array(    
                array('id'=>1563,'value'=>$argv[1])     
            )   
        );  
      
$post = array(  
        'apikey' =>"0635d163f4c298d4383e50e8902d0f5a",  
         'params'=>$params  
    );  
          
$ch = curl_init();  
curl_setopt($ch, CURLOPT_URL, $url);  
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);  
curl_setopt($ch, CURLOPT_POST, 1);  
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);  
$result = json_decode(curl_exec($ch));  
curl_close ($ch);  
echo(json_encode($result,JSON_UNESCAPED_UNICODE));


