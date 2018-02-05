---
layout: post
comments: true
title:  "Javascript Aspect Toolkit-2"
date:   2018-02-05 19:24:00
author: 김지운
cover:  "/assets/instacode.png"
---

AOP 에 대한 내용을 하다가 커뮤니티에서 논쟁이 된 내용을 이야기하느라 못한 이야기를 적는다.
[AOP.js]에서 레파지토리를 클론한다. 혹은 그냥 다운받는다.

##### AOP.js
```javascript
// Created by Fredrik Appelberg: http://fredrik.appelberg.me/2010/05/07/aop-js.html
// Modified to support prototypes by Dave Clayton
Aop = {
  // Apply around advice to all matching functions in the given namespaces
  around: function(pointcut, advice, namespaces) {
    // if no namespaces are supplied, use a trick to determine the global ns
    if (namespaces == undefined || namespaces.length == 0)
      namespaces = [ (function(){return this;}).call() ];
    // loop over all namespaces
    for(var i in namespaces) {
      var ns = namespaces[i];
      for(var member in ns) {
        if(typeof ns[member] == 'function' && member.match(pointcut)) {
          (function(fn, fnName, ns) {
             // replace the member fn slot with a wrapper which calls
             // the 'advice' Function
             ns[fnName] = function() {
               return advice.call(this, { fn: fn,
                                          fnName: fnName,
                                          arguments: arguments });
             };
           })(ns[member], member, ns);
        }
      }
    }
  },

  next: function(f) {
    return f.fn.apply(this, f.arguments);
  }
};

Aop.before = function(pointcut, advice, namespaces) {
  Aop.around(pointcut,
             function(f) {
               advice.apply(this, f.arguments);
               return Aop.next.call(this, f);
             },
             namespaces);
};

Aop.after = function(pointcut, advice, namespaces) {
  Aop.around(pointcut,
             function(f) {
               var ret = Aop.next.call(this, f);
               advice.apply(this, f.arguments);
               return ret;
             },
             namespaces);
};

module.exports = Aop;
```

|용어|의미|
|---|---|
|Advice|배포할 코드 조각|
|Aspect|Advice 가 처리할 문제|
|cross-cutting concern|Aspect 와 동일|
|Target|부가기능을 부여할 대상으로 핵심기능이 담긴 클래스이거나 추가적인 부가기능을 제공할 프록시 오브젝트 일 수 있다|
|Join Point|Advice 가 적용될 위치. 타깃 오브젝트가 구현한 인터페이스의 모든 메서드가 조인 포인트가 된다.|
|Point Cut|Join Point 를 선별하는 기능을 정의한 모듈|
|Proxy|클라이언트와 타깃 사이에 존재하면서 부가기능을 제공하는 오브젝트. 클라이언트는 타깃을 요청하지만, 클라이언트에게는 DI를 통해 타깃 대신 프록시가 주입된다. 클라이언트의 메소드 호출을 대신 받아서 타깃에게 위임하며, 그 과정에서 부가기능을 부여한다. 스프링 AOP는 프록시를 이용한다.|
|Advisor|포인트컷과 어드바이스를 하나씩 갖고 있는 오브젝트. AOP의 가장 기본이 되는 모듈이다. 스프링은 자동 프록시 생성기가 어드바이저 단위로 검색해서 AOP를 적용한다.|

출처 : [AOP(Aspect Oriented Programming)]

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```

AOP.js 를 보면 주어진 namespace 를 순회하며 Advice 를 적용할 곳을 찾고 적용한다.
우리가 의존성을 주입한 코드들은 모두 실행된다. 언제 실행되냐에 대해서 결정하는 것이 AOP 의 핵심이다.

책에서는 이를 분석하는 도구로 TDD 를 이용하는 과정을 설명한다.

일단 책에 코드는 ES 를 사용하지 않았다. 그래서 ES 와 섞어 짜고 있는 부분에서 주의할 점을 먼저 이야기한다.
일단 Arrow function 은 생성자에서 사용하지 못한다. 구문에러가 발생할 것이다.
그리고 책에서는 arguments 를 이용하여 인자를 조작하는데 Arrow function 을 이용하게 되면 arguments 를 제어하는 다른 방법을 제공하므로 arguments 를 사용하게 되면 undefined 일것이다.

그 외의 부분은 Arrow function 을 이용할 것이다.

##### AOP_02.js
```javascript
Aop = {
    around:function(fnName, advice, fnObj){
        // Done
        let originalFn = fnObj[fnName];
        fnObj[fnName] =  function() {
            let targetContext = {};
            return advice.call(targetContext,{fn:originalFn, args:arguments});
        };
    }
};
```
##### AOP_tests_02.js
```javascript
describe('Aop',()=>{

    let argPassingAdvice; // 타깃에 인자를 전달할 어드바이스
    let argsToTarget; // targetObj.targetFn 에 전달할 인자들
    let targetObj;
    let executionPoints;
    let targetFnReturn = 123;
    beforeEach(()=>{
        targetObj = {
            targetFn:function(){
                executionPoints.push('targetFn');
                argsToTarget = Array.prototype.slice.call(arguments, 0);
                return targetFnReturn;
            }
        };
        executionPoints = [];

        argPassingAdvice = (targetInfo)=>{
            return targetInfo.fn.apply(this, targetInfo.args);
        };
        argsToTarget = [];
    });

    describe('Aop.around(fnName, advice, targetObj)',()=>{
        it('타깃 함수 호출 시 어드바이스를 실행하도록 한다.', ()=>{

            let excuteAdvice = false;
            let advice = ()=>{
                excuteAdvice = true;
            };
            Aop.around('targetFn',advice,targetObj);
            targetObj.targetFn();
            expect(excuteAdvice).toBe(true);
        });
        it('어드바이스가 타깃 호출을 래핑한다.',()=>{
            let wrappingAdvice = (targetInfo)=>{
                executionPoints.push('wrappingAdvice - 처음');
                targetInfo.fn();
                executionPoints.push('wrappingAdvice - 끝');
            };
            Aop.around('targetFn',wrappingAdvice,targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual(['wrappingAdvice - 처음','targetFn','wrappingAdvice - 끝']);

        });
        it('마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.',()=>{
            const adviceFactory = (adviceId)=>{
                return ((targetInfo)=>{
                    executionPoints.push('wrappingAdvice - 처음 '+adviceId);
                    targetInfo.fn();
                    executionPoints.push('wrappingAdvice - 끝 '+adviceId);
                });
            };
            Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
            Aop.around('targetFn',adviceFactory('바깥쪽'), targetObj);
            targetObj.targetFn();
            expect(executionPoints).toEqual([
                'wrappingAdvice - 처음 바깥쪽',
                'wrappingAdvice - 처음 안쪽',
                'targetFn',
                'wrappingAdvice - 끝 안쪽',
                'wrappingAdvice - 끝 바깥쪽'
            ]);
        });
        it('어드바이스에서 타깃으로 일반 인자를 넘길 수 있다',()=>{

            Aop.around('targetFn',argPassingAdvice,targetObj);
            targetObj.targetFn('a', 'b');
            expect(argsToTarget).toEqual(['a','b']);
        });
        it('타깃의 반환값도 어드바이스에서 참조 할 수 있다.',()=>{

            Aop.around('targetFn', argPassingAdvice, targetObj);
            const returnedValue = targetObj.targetFn();
            expect(returnedValue).toBe(targetFnReturn);
        });
    });

});
```

실제 모듈에는 module.exports 로 commonjs 스타일로도 모듈을 추출하고 있다.
일단은 순서대로 위 테스트를 통과하도록 짜본 결과이다. 책의 코드들이 앞에서와 마찬가지로 작동하지 않는 코드들이 있다. 읽을 때 참고해야할듯 하다.

각 테스트별 수행 작업은 아래 리스트를 참고한다.

- **타깃 함수 호출 시 어드바이스를 실행하도록 한다.**

    - ```javascript
      let targetObj;
      let executionPoints;
      ```
      ```javascript
      beforeEach(()=>{
              targetObj = {
                  targetFn:function(){
                      executionPoints.push('targetFn');
                  }
              };
              executionPoints = [];
          });
      ```
      ```javascript
       it('타깃 함수 호출 시 어드바이스를 실행하도록 한다.', ()=>{

                   let excuteAdvice = false;
                   let advice = ()=>{
                       excuteAdvice = true;
                   };
                   Aop.around('targetFn',advice,targetObj);
                   targetObj.targetFn();
                   expect(excuteAdvice).toBe(true);
               });
      ```
      일단 외부에서 Advice 를 주입할 PointCut 에 해당하는 함수 이름을 TargetFn 으로 한다.
      그리고 타깃 객체를 하나 초기화 한다.

      그리고 실행 여부를 확인할 boolean 값을 가지는 변수를 하나 생성한다.
      실행 여부만 확인하면 되니 간단하게 실행되면 excuteAdvice 를 true 로 변경해주는 Advice 를 작성한다.
      그리고 AOP 는 아래와 같이 작성한다.
      ```javascript
      Aop = {
        around: function(fnName, advice, fnObj) {
          fnObj[fnName] = advice;
        }
      };
      ```
      타겟 오브젝트의 targetFn 을 제공된 advice 로 변경하고 테스트에서는 변경된 targetFn 을 호출하게된다.
      그러므로 excuteAdvice 는 true 가 된다.
- **어드바이스가 타깃 호출을 래핑한다.**

    - ```javascript
      Aop = {
        around: function(fnName, advice, fnObj) {
          var originalFn = fnObj[fnName];
          fnObj[fnName] = function () {
            var targetContext = {};
            advice.call(targetContext, {fn:originalFn});
          };
        }
      };
      ```

      ```javascript
      it('어드바이스가 타깃 호출을 래핑한다.',()=>{
                  let wrappingAdvice = (targetInfo)=>{
                      executionPoints.push('wrappingAdvice - 처음');
                      targetInfo.fn();
                      executionPoints.push('wrappingAdvice - 끝');
                  };
                  Aop.around('targetFn',wrappingAdvice,targetObj);
                  targetObj.targetFn();
                  expect(executionPoints).toEqual(['wrappingAdvice - 처음','targetFn','wrappingAdvice - 끝']);

              });
      ```
      전달된 advice 의 실행전에 targetObj 의 원래 함수를 저장하고 advice 의 호출을 call 로 인자로 실행 컨텍스트와 fn 에 앞에서 저장한 originalFN 을 가지는 Object 를 전달한다.
      advice 로 전달된 wrappingAdvice 의 targetInfo 에 {fn:originalFn} 이 전달되고 이를 targetInfo 로 받아서 실행하여 originalFn 을 래핑하는 wrappingAdvice 가 정상적으로 실행된다.
- **마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.**

    - ```javascript
      it('마지막 어드바이스가 기존 어드바이스에 대해 실행되는 방식으로 체이닝 할 수 있다.',()=>{
                  const adviceFactory = (adviceId)=>{
                      return ((targetInfo)=>{
                          executionPoints.push('wrappingAdvice - 처음 '+adviceId);
                          targetInfo.fn();
                          executionPoints.push('wrappingAdvice - 끝 '+adviceId);
                      });
                  };
                  Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
                  Aop.around('targetFn',adviceFactory('바깥쪽'), targetObj);
                  targetObj.targetFn();
                  expect(executionPoints).toEqual([
                      'wrappingAdvice - 처음 바깥쪽',
                      'wrappingAdvice - 처음 안쪽',
                      'targetFn',
                      'wrappingAdvice - 끝 안쪽',
                      'wrappingAdvice - 끝 바깥쪽'
                  ]);
              });
      ```
      위 **어드바이스가 타깃 호출을 래핑한다.** 와 Aop 코드는 같다.

      advice 를 여러개 제공할거기 때문에 advice 를 제공할 adviceFactory 를 만들었다.
      adviceFactory 는 인자로 adviceId 를 전달받고 나머지는 이전에 advice 와 똑같다.

      ```javascript
      {
         targetFn:function(){
            executionPoints.push('targetFn');
         }
      };
      ```

      targetObj 는 처음에 위와 같은 targetFn 을 가지는 Object 이다.
      advice 를 주입하는 Aop.around(함수이름, 어드바이스, 오브젝트) 를 통해 처음으로
      ```javascript
      Aop.around('targetFn',adviceFactory('안쪽'), targetObj);
      ```
      를 호출하게 되면 targetObj 는 아래처럼 제공된 advice 로 변경이 되게된다.
      ##### adviceId = '안쪽' 일때의 targetObj.targetFn()
      ```javascript
      (targetInfo)=>{
          executionPoints.push('wrappingAdvice - 처음 '+adviceId);
          //targetInfo.fn(); 은
          //function(){
          //    executionPoints.push('targetFn');
          //}
          //을 호출
          targetInfo.fn();
          executionPoints.push('wrappingAdvice - 끝 '+adviceId);
      }
      ```
      targetInfo 는 위에서 설명 했듯이 .call(this, arg1,arg2,...) 으로 인해
      targetObj 의 원래의 targetFn 이 된다. 그리고 나서 다시한번 adviceId 를 변경한 advice 를 전달하면 최종적으로 아래와 같이 실행된다.
      ```javascript
      (targetInfo)=>{
          executionPoints.push('wrappingAdvice - 처음 '+adviceId);
          //targetInfo.fn(); 은
          //(targetInfo)=>{
          //    executionPoints.push('wrappingAdvice - 처음 '+adviceId);
          //    //targetInfo.fn(); 은
          //    //function(){
          //    //    executionPoints.push('targetFn');
          //    //};
          //    //을 호출
          //    targetInfo.fn();
          //    executionPoints.push('wrappingAdvice - 끝 '+adviceId);
          //};
          //을 호출
          targetInfo.fn();
          executionPoints.push('wrappingAdvice - 끝 '+adviceId);
      }
      ```

- **어드바이스에서 타깃으로 일반 인자를 넘길 수 있다**

- **타깃의 반환값도 어드바이스에서 참조 할 수 있다.**

[AOP(Aspect Oriented Programming)]:http://blog.naver.com/PostView.nhn?blogId=kbh3983&logNo=220836425242
[AOP.js]:https://github.com/davedx/aop
