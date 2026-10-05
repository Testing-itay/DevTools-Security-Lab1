<?php

const REPORT_ROOT = '/var/reports';

function restore_report_state()
{
    $state = unserialize($_GET['state']);
    return $state;
}

function render_report_title()
{
    echo '<h1>' . $_GET['title'] . '</h1>';
}

function finish_report_flow()
{
    header('Location: ' . $_GET['return_to']);
    exit;
}

function fetch_remote_dataset()
{
    $body = file_get_contents($_GET['dataset_url']);
    return $body;
}

function store_uploaded_report()
{
    move_uploaded_file($_FILES['report']['tmp_name'], REPORT_ROOT . '/' . $_FILES['report']['name']);
    return $_FILES['report']['name'];
}

function apply_report_filters()
{
    extract($_GET);
    return isset($filter) ? $filter : null;
}
