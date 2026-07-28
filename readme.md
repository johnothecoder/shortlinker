# Short Linker (`shrtlnkr`)

<p align="center">
    <a href="https://jtclabs.com/projects/shrtlnkr">
        <img src="shrtlnk/static/shrtlnk/images/shrtlnkr.png" alt="shrtlnkr" width="250">
    </a>
</p>



**Description** A small Python/Django URL shortener and click tracker. 

**License** Open source on an [MIT license](license.md)

**Base Tech** [Python - Django Framework](https://www.djangoproject.com/) and [PostgreSQL](https://www.postgresql.org/)

**Author** [JohnoTheCoder](https://github.com/johnothecoder) @ [JTC Labs](https://jtclabs.com)

**More Info** [shrtlnkr](https://jtclabs.com/projects/shrtlnkr)

---

Create short links through the Django admin, track every redirect, and optionally collect additional client-side metadata (such as browser-provided location) after the redirect.

Originally written to support QR code signup tracking for posters, flyers and printed media.

Temu Bitly for people who know a guy/girl/human/bot who can host a Python project for them.

---

I do not foresee or intend this being widely adopted, if it gets a bunch of stars maybe I'll write some more useful documentation here. 

You're welcome to use it, but you do so at your own risk. This isn't WordPress, Laravel, or Django; I'm just a boy, sitting in front of PyCharm, writing some code, hoping his {Generic Sugar Free Energy Drink} is still cold.

## Why build shrtlnkr?

1. Felt like it
2. Does exactly what I want, how I want, 'cause I wrote it
3. Seemed less effort than the investigative process of finding an alternative
4. Didn't feel like doing `3`, spent 3 minutes, found 47 unmaintained repositories or didn't trust "we compiled it for you... just install it"
5. Python/Django choice, basically `1`... love Laravel, didn't feel like paying for Nova (which is beautiful, tbf), Rails felt a bit much for this one

# V1 Requirements

Managing base requirements here rather than adding the admin burden of managing issues and statuses.

**KEY:** Not completed // ~~Completed Task~~

- [x] Add a link with a custom unique `slug`
- [x] Be able to remove/deactivate said link
- [x] User visits `host.tld/c/{slug}` the user is redirected to the relevant destination
- [x] Relevant destination has a unique identifier attached. Default parameter is `clickid`; this is configurable via `.env`
- [x] Redirects are tracked
- [x] Click IDs should be UUID v4
- [ ] `[Optional]` A one-time endpoint is available that allows update of the click record (e.g. if location tracking information is available)
- [ ] `[Optional]` Send a scheduled report of how many clicks there have been (probably weekly)
- [x] Landing page for users hitting the root domain
- [x] Friendly 404 handling
- [ ] Admin Dashboard of some description to give an overview
- [x] Allow Query String Proxy 
