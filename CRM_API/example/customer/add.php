<?php
/*********************************** 
 ** Добавление новых контактов 
 ** Пример: Добавление двух контактов   
**********************************/  
  
$url='http://amls.intrumnet.com:81/sharedapi/purchaser/insert';  
  
$params=array(  
            array(  
                'manager_id '=>0, // без привязки к ответственному  
                'name'=> $argv[1],    
                'phone' => array($argv[2]),
                'fields' => array(    
                    array('id'=>1560,'value'=>$argv[3]),
                    array('id'=>1561,'value'=>$argv[4]),
                    array('id'=>1563,'value'=>$argv[5])     
                )
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
echo(json_encode($result,JSON_UNESCAPED_UNICODE));
curl_close ($ch);  
?>
