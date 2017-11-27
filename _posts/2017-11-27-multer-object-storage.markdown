---
layout: post
title:  "Node js & ObjectStroage(openstack) & multer"
date:   2017-11-27 22:08:43
author: 김지운
cover:  "/assets/instacode.png"
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

