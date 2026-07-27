# Short Linker (`shrtlnkr`)

I do not foresee or intend this being widely adopted, if it gets a bunch of stars maybe I'll write some more useful documentation here. There is zero rocket science within this repository.

You're welcome to use it, but you do so at your own risk. This isn't WordPress, Laravel, or Django; I'm just a boy, sitting in front of PyCharm, writing some code, and hoping it doesn't error.

## Why build shrtlnkr?

1. Felt like it
2. Does exactly what I want, how I want, 'cause I wrote it
3. Seemed less effort than the investigative process of finding an alternative
4. Didn't feel like doing `3`
5. Python/Django choice, basically `1`... love Laravel, didn't feel like paying for Nova (which is beautiful, tbf), Rails felt a bit much for this one

# V1 Requirements

Managing base requirements here rather than adding the admin burden of managing issues and statuses.

**KEY:** Not completed // ~~Completed Task~~

1. Add a link with a custom unique `slug`
2. Be able to remove/deactivate said link
3. User visits `host.tld/c/{slug}` the user is redirected to the relevant destination
4. Relevant destination has a unique identifier attached. Default parameter is `clickid`; this is configurable via `.env`
5. Redirects are tracked
6. `[Optional]` A one-time endpoint is available that allows update of the click record (e.g. if location tracking information is available)
7. Click IDs should be UUID v4

# Tech Stack

1. Python 3 & Django Framework 
2. PostgreSQL
3. Check `requirements.txt`

# License

MIT License

Copyright (c) 2026 Matt Johnson t/a JohnoTheCoder & JTC Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.