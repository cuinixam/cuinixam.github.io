---
title: "How to create your GitHub Pages site with Jekyll"
excerpt: "Create you own GitHub Pages site is trivial. One only needs to use a template, adapt, generate and test it locally before deploying it to GitHub."
categories:
  - howto
tags:
  - Jekyll
  - ghpages
  - github
---

* toc
{:toc}

# Create the GitHub Pages site repository

The simplest way to getting started is to use a template.
I have used [Minimal Mistakes][minimal-mistakes] to create this site.

Click [here][mm-generate-from-template] to create a new repository using the same theme.

**NOTE:** When you are creating a GitHub Pages user site, your repository must be named `<user>.github.io`.
{: .notice--info }

After creating the repository, clone and adapt it to your needs. The [Minimal Mistakes][minimal-mistakes] documentation is a very good starting point.

# Build your site locally

Install Ruby with the [official installer](https://rubyinstaller.org/downloads/) and not with ``scoop`` or other self hacked Windows installer.

Switch to the repository root directory and install all dependencies with

```
bundle install
```

In order to build the page and serve it on the localhost run

```
bundle exec jekyll serve
```

If everything worked you should see something like:

```
  Server address: http://127.0.0.1:4000
  Server running... press ctrl-c to stop.
```


## Troubleshooting

 
* If this fails with ``GitHub Metadata: No GitHub API authentication could be found. Some fields may be missing or have incorrect data.`` you need to add `github: [metadata]` to the  ``_config.yml`` file in the project.

* In case the command fails with some missing Ruby packages just install them. I was missing ``webrick`` and I installed it by running ``bundle add webrick``.


[minimal-mistakes]: https://mademistakes.com/work/minimal-mistakes-jekyll-theme/
[mm-generate-from-template]: https://github.com/mmistakes/mm-github-pages-starter/generate

