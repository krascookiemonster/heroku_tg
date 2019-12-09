<?php
    /* Вариант использования без composer*/
	require_once  dirname( __FILE__ ).'../../Intrum/Api.php';
	require_once  dirname( __FILE__ ).'../../Intrum/Cache.php';
	
	/*Intrum\Cache::getInstance()->setup(
		array(
			"folder" => __DIR__ . "/cache",
			"expire" => 600
		)
	);*/
	
	$api = Intrum\Api::getInstance()
	->setup(
		array(
			"host"   => "amls.intrumnet.com",//"yourdomain.intrumnet.com",
			"apikey" => "0635d163f4c298d4383e50e8902d0f5a",
			"cache"  => false,
			"port"   => 80
		)
	);
?>