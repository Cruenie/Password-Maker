<h1 align="center">
What is PassMaker?
</h1>

<p>
  PassMaker is a tool to create secure (hopefully), 16 char long passwords that utilize hashes and private keys to create unique passwords for each user, for each website, for each account so that you don't need to trust some web service that is conveniently storing all your passwords and can be accessed by any of your devices :3
</p>

<h1 align="center">
  How to use PassMaker?
</h1>

## You need to create a .env file with 2 fields: SIGNS and KEY, like so:


```bash
SIGNS = '*.F_æÇ">*='
KEY = 'ilovecats'
```
SIGNS should include 10 special characters, and your KEY can be anything, as long as you keep it the same.

After running the program, you will be asked a URL. This is then parsed and used to create your unique password for that website.

You can use the URL of the login page, URL of the main page, URL of a specific page, it doesn't matter as long as you input the same page, you will get the same unique password.

## If you have more than one account on that website, you can:

* Add a numer after the webpage: www.example_2.com
* Add your nickname into the mix: www.example_coolnick.com
* Add your nickname into the mix: cool_nick@example.com
* or anthing, as long as you change the URL, you will get a unique password.

##  Example*

When you run the program using these .env variables


```bash
SIGNS = '½#}_->$+ßæ'
KEY = 'cats'
```
and input 

```
google.com
```

Note: google.com and www.google.com will result in different passwords.

You get:
```
7-bæeæ3½2}7+1_a}
```
Every time you run the program with the same parameters, it will result in the same password, so you can login safely.


Please note that in the future versions, the algorithm may change, causing you to lose your passwords. Make sure to use the same version. Updating your passwords with each version is recommended.


*: Examples are outdated. The program holds integrity, just works in a different way now.


<h1 align="center">
  Notes
</h1>

* Inputting https://google and google will change the output.
* Adding tailing spaces to anything (KEY, URL...) will change the output.
* The program doesn't log keys, so be careful while changing them since you may have to change your passwords.
* Experiment with the program. You can put the URL inside the KEY and put your KEY as an input, you can do whatever you want with this software. Stay secure!
  
