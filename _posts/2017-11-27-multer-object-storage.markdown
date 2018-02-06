---
layout: post
title:  "multer 확장 스토리지 엔진"
date:   2017-11-27 22:08:43
author: 김지운
cover:  "/assets/instacode.png"
categories: Post
---

### Object Storage Engine

node js에서 multipart/form-data 처리시 [multiparty](https://github.com/pillarjs/multiparty)를 많이 이용하였는데 star수도 그렇고 업데이트 되는 속도도 느려서
[multer](https://github.com/expressjs/multer)로 갈아타게 되었다.

헌데 multer에서 ObjectStorage(OpenStack)접근하는 코드를 바로 제공하지는 않고 확장해서 사용할 수 있게 해놔서 확장 코드를 작성해 보았다.
해당 코드는 테스트 해볼 수 있게 express 프로젝트로 만들어서 깃헙에 배포했다.

[깃헙 링크](https://github.com/kishe89/MulterObjectStorageEngine)

{% highlight javascript %}
function ObjectStorage (opts) {
    this.getDestination = (opts.destination)
}

ObjectStorage.prototype._handleFile = function _handleFile (req, file, cb) {
    this.getDestination(req, file, function (err, container) {
        if (err) {
            return cb(err)
        }
        let outStream = req.storageClient.upload({
            container:container,
            remote:file.originalname
        });
        file.stream.pipe(outStream);
        outStream.on('error', cb)
        outStream.on('success', function (savedFile) {
            cb(null, {
                container: container,
                path: savedFile.name,
                size: savedFile.size,
                date:Date.now()
            })
        })
    })
}
ObjectStorage.prototype._removeFile = function _removeFile (req, file, cb) {
    req.storageClient.removeFile({
        container:file.container,
        remote:file.originalname
    },()=>{
        cb(null, {
            container: container,
            path: file.originalname,
            date:Date.now()
        })
    })
}
module.exports = function (opts) {
    return new ObjectStorage(opts)
}
{% endhighlight %}

위 코드는 multer에서 확장 가능한 스토리지 엔진을 구현할 때 꼭 구현해줘야하는 부분만 구현해놓았다.

{% highlight javascript %}
function ObjectStorage (opts) {
    this.getDestination = (opts.destination)
}
module.exports = function (opts) {
    return new ObjectStorage(opts)
}
{% endhighlight %}

위 코드는 options를 받아서 options에 있는 destination property를 해당 storage engine 인스턴스에 세팅하고 exports하는 부분이다.
multer는 내부적으로 storage를 세팅할 수 있게 storage라는 key로 storage 들을 받을 수 있게 구현 되어있는데 이 때 storage engine 기본 제공하는것이
memory storage, runtime file storage를 제공하는데 이외의 확장 storage를 해당 key 셋할 수 있다.

{% highlight javascript %}
const storageEngine = require('../util/ObjectStorageEngine');
const upload = multer({
    storage:storageEngine({
        destination:  (req, file, cb)=> {
            cb(null, 'profile')
        }
    })
});
{% endhighlight %}

위 코드는 구현한 storage engine을 로드해서 multer의 보면 destination에 req, file, cb를 받는 함수를 넘겨주게 되는데 이 함수가 storage engine의
getDestination에 세팅된다. 이 getDestination property는 storage engine 구현시 꼭 구현해야하는 함수중 하나인 _handleFile안에서 사용하게 되는데
multipart/form-data로 받은 파일들이 하나씩 넘어오게 된다.

{% highlight javascript %}
ObjectStorage.prototype._handleFile = function _handleFile (req, file, cb) {
    this.getDestination(req, file, function (err, container) {
        if (err) {
            return cb(err)
        }
        let outStream = req.storageClient.upload({
            container:container,
            remote:file.originalname
        });
        file.stream.pipe(outStream);
        outStream.on('error', cb)
        outStream.on('success', function (savedFile) {
            cb(null, {
                container: container,
                path: savedFile.name,
                size: savedFile.size,
                date:Date.now()
            })
        })
    })
}
{% endhighlight %}

넘어온 파일은 stream(readable)을 가지고 있는데 이를 우리가 저장할 storage에 writable한
stream(위 소스에서는 pkgcloud client 사용)과 연결해주면 파일의 저장은 완료된다.

pkgcloud의 자세한 사용법은 [pkgcloud깃헙](https://github.com/pkgcloud/pkgcloud)를 참고하면 된다.

{% highlight javascript %}
ObjectStorage.prototype._removeFile = function _removeFile (req, file, cb) {
    req.storageClient.removeFile({
        container:file.container,
        remote:file.originalname
    },()=>{
        cb(null, {
            container: container,
            path: file.originalname,
            date:Date.now()
        })
    })
}
{% endhighlight %}

마지막으로 _removeFile 함수 또한 구현해야하는데 이는 위 코드처럼 파일 삭제에 대한 구현을 해주면 된다.
