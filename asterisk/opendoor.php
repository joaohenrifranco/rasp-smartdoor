#!/usr/bin/php -q
<?php
require ("/etc/asterisk/phpagi/phpagi.php");

define("API_ADDR", "192.168.88.41/api/request-front-door-unlock");

function sendUnlockRequest($sip) {
    $sip_array = ["sip" => $sip,];
    $sip_json = json_encode($sip_array); 
    $ch = curl_init(API_ADDR);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $sip_json);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        "Content-Type: application/json",
        "Content-Length: " . strlen($sip_json))
    );
    $response = curl_exec ($ch);
    $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close ($ch);

    if ($http_status == "200") {
        $response_array = json_decode($response, true);
        return $response_array['status'];
    }
    return -1;
}

$agi = new AGI();
$asterisk_response = $agi->get_variable('CALLERID(number)');
$sip = $asterisk_response["data"];
$status = sendUnlockRequest($sip);
$agi->verbose($status);
if ($status == 10) {
  $agi->exec("SendDTMF","*1337#");
    
}


?>
