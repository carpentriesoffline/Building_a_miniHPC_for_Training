# Jekyll Template

Use this template and expand on it if you want to create a Jekyll webpage.

1. The easiest way that I found to work with Jekyll pages is to use the Jekyll docker image. Start by pulling the image:

  ```docker pull jekyll/jekyll```
1. Now create your own repository by using this repository as a template. Click on the green ```Use this template``` button.
1. Clone the new repository to your harddrive. Let's say you clone it to ```/home/you/mywebsite```.
1. To serve the website type the following in the command line:
  ```export JEKYLL_VERSION=3.8
  docker run --rm --name jekyll --volume="/home/you/mywebsite:/srv/jekyll" --publish 4000:4000 jekyll/jekyll jekyll serve
  ```
4. You can now edit any of the files. As soon as you save the site will be rebuilt and you can view it on ```http://localhost:4000```
1. Obviously you should replace all instances of ```/home/you/mywebsite``` with the name of the directory where you actually are saving the files.
1. Make sure you set the source branch for building GitHub pages to ```main```. This can be done by clicking on ```Settings```, i.e. Settings for the project and not for your GitHub account. Then, click on ```Pages```. Look for the heading **Source** and select ```Branch:main```. Save the change.
