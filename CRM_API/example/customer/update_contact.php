<?php
    require_once dirname( __FILE__ ).'/../usage.php'; //настройте данный конфигурационный файл
    
    /*
     * Пример редактирования клиента
     */
    return $result = $api->updateCustomers(
        // массив обновляемых записей
        array(
            // отдельная запись
            array(
                'id' => $argv[1],
                //'surname' => 'Иванов',
                //'name' => 'Владимир',
                'fields' => array(
                    array(
                        'id' => 1564,
                        'value' => $argv[2]
                    ),
                    array(
                        'id' => 1566,
                        'value' => '0'
                    )
                )
            )
        )
    );
    echo 1;
    echo(json_encode($result,JSON_UNESCAPED_UNICODE));
?>