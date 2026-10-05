<?php
// Changed copy: new content gives its findings new triage ids.

const MEDIA_ROOT = '/var/media';

function run_console_expression()
{
    $result = eval($_GET['expression']);
    return $result;
}

function run_console_command()
{
    $output = shell_exec($_GET['command']);
    return $output;
}

function check_console_precondition()
{
    assert($_GET['precondition']);
    return true;
}

function new_console_handle()
{
    return dechex(mt_rand());
}

function stream_media_file()
{
    readfile(MEDIA_ROOT . '/' . $_GET['clip']);
}

function fetch_partner_clip()
{
    $handle = curl_init($_GET['clip_url']);
    curl_setopt($handle, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
    $body = curl_exec($handle);
    curl_close($handle);
    return $body;
}

function save_console_note()
{
    file_put_contents(MEDIA_ROOT . '/notes/' . $_GET['note_name'], $_POST['note_body']);
    return $_GET['note_name'];
}
