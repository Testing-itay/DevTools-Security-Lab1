<?php

function find_account_by_email($mysqli)
{
    $email = $_GET['email'];
    return $mysqli->query("SELECT id, name FROM accounts WHERE email = '" . $email . "'");
}

function run_account_maintenance()
{
    $task = $_GET['task'];
    exec("account-maint --run " . $task, $output);
    return $output;
}

function render_account_greeting()
{
    echo "Welcome back, " . $_GET['name'];
}

function load_account_template()
{
    include "/var/portal/templates/" . $_GET['template'];
}

function fetch_account_avatar()
{
    return file_get_contents($_GET['avatar_url']);
}
