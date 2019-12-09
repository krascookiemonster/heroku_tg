<?php

/*
 *  Пример добавления комментария
 */

require_once '../usage.php'; 

$res = $api->addSalesComment(array(
    'enity_id' => 272, //ID объекта в Интруме
    'text'     => "Новый комментарий", //Текст комментария
    'author'   => 2, //ID ползователя в Интруме, от чьего имени будет комментарий, если передать 0, комментарий будет от имени системы,
));

print_r($res);
