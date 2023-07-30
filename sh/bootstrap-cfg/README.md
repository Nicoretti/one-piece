# Bootstrap the terminal-conifg environment
```curl https://raw.githubusercontent.com/Nicoretti/one-piece/grand-line/sh/bootstrap-cfg/bootstrap.sh | sh```

**Attention:**
*VIM/NVIM* need an additional call to PlugUpdate on the first run.

## What is this project all about
Due to the fact that  everything in my terminal-config project ends up to be in my home, this project is used
to seperatly provide a bootstrap script and documentation for my terminal-config (dotfile) environment.

## The Technique I use for my dotfile setup
The technique I use I was pointed to by [flxo](https://github.com/flxo) he shared this
[blog post](https://developer.atlassian.com/blog/2016/02/best-way-to-store-dotfiles-git-bare-repo/)
with me which is a game changer, at least I have been for me. What did I use/try before?

copy, git + copy, git + symlinks, git + custom config + symlinks, etc.

* [cp](http://man7.org/linux/man-pages/man1/cp.1.html)
* [ln](http://man7.org/linux/man-pages/man1/ln.1.html)
* [git](https://git-scm.com/)
* [config-installer](https://github.com/Nicoretti/config-installer)
* [gnu stow](https://www.gnu.org/software/stow/) 

## The config/dotfile repository
My config file(s) can be found [here](https://github.com/Nicoretti/terminal-config)

## Simillar alternatives

### YADM (Yet Another Dotfile Manager)
If you are not interested in getting the gist behind the technique and rather want something that just works 
out of the box nicely, use YADM. It also comes with nice additonal cmd tooling like encryption out of the box.
Details can be found [here](https://thelocehiliosan.github.io/yadm/)


