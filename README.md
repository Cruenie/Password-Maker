## What is Pass Maker?
<p>
  Pass Maker is a tool to create secure (hopefully) passwords that utilize hashes and private keys to create unique passwords for each user, for each website, for each account so that you don't need to trust some web service that is reliably storing all your passwords and can be accessed by any of your devices :3
</p>

## How to use PassMaker?
<h3 align="center">
  You need to create a .env file with 2 fields: SIGNS and KEY, like so:
</h3>

```bash
SIGNS = '*.F_æÇ">*='
KEY = 'ilovecats'
```
<p>
  SIGNS should include 10 special characters, and your KEY can be anything, as long as you keep it the same.
</p>
<p>
  After running the program, you will be asked a URL. This is then parsed and used to create your unique password for that website.
</p>
<p>
  You can use the URL of the login page, URL of the main page, URL of a specific page, it doesn't matter as long as you input the same page, you will get the same unique password.
</p>
<p>
   
</p>
<p>
  <h3 align="center">
    If you have more than one account on that website, you can:
  </h3>
  <p>Add a numer after the webpage: www.example_2.com</p>
  <p>Add your nickname into the mix: www.example_coolnick.com</p>
  <p>or anthing, as long as you change the URL, you will get a unique password.</p>
</p>

## Examples
When you run the program using these .env variables
```bash
SIGNS = '½#}_->$+ßæ'
KEY = 'cats'
```
and input 
```bash
google.com
```
Note: google.com and www.google.com will result in different passwords.

You get:
```bash
7#3@2@6#a@f|3|2}
```
<p>Every time you run the program with the same parameters, it will result in the same password, so you can login safely.
</p>
