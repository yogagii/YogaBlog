Title: Network and Multithread
Date: 2020-03-26
Category: IOS
Tags: Swift
Author: Yoga

load view -> fetch data(Network) -> save data -> display(Multithread) -> action

## WebView 可以装网页的容器

网页中的代码可以和原生应用代码交互

UIwebview 有内存泄漏的问题，苹果优化做了 webkitbweview

```
  class WebViewController: UIViewController, WKUIDelegate, WKNavigationDelegate {

    var webView: WKWebView!

    override func viewDidLoad() {
        super.viewDidLoad()

        let webConfig = WKWebViewConfiguration()
        webView = WKWebView(frame: CGRect(x: 0, y: 88, width: view.frame.width, height: view.frame.height - 88), configuration: webConfig)
        webView.uiDelegate = self
        webView.navigationDelegate = self
        view.addSubview(webView)

//        let url = URL(string: "https://cn.bing.com/")
        let fileUrl = Bundle.main.url(forResource: "test", withExtension: "html")
        let myRequest = URLRequest(url: fileUrl!)
        webView.load(myRequest)

webView.configuration.userContentController.add(self, name: "getMessage")
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        self.webView.evaluateJavaScript("alert(\"hihi\")") { (data, error) in
            print(error)
        }
    }

    func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping () -> Void) {
        let alertVc = UIAlertController(title: "Alert", message: message, preferredStyle: .alert)
        alertVc.addAction(UIAlertAction(title: "ok", style: .default, handler: { (action) in
            completionHandler()
        }))
        self.present(alertVc, animated: true) {

        }
    }

    deinit {
        print("💢 \(self) is deinit!!!")
    }
}

```

网页的 iframe 相当于去服务器访问，所以有跨域问题

手机的 webview 都是本手机访问，所以没有跨域问题

性能问题：

强引用(不会 deinit);

WebViewController -> WebView -> ScriptMessageHandler -> WebViewController

弱引用

WebViewController -> WebView -> ScriptMessageHandler -> WeekHandler ...>弱引用...> WebViewController

```
  class WebViewController: UIViewController, WKUIDelegate, WKNavigationDelegate, WKScriptMessageHandler {
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        <#code#>
    }

        webView.configuration.userContentController.add(WeekScriptMessageDelegate(self), name: "getMessage")
//webView.configuration.userContentController.add(self, name: "getMessage")
    }
}

class WeekScriptMessageDelegate: NSObject, WKScriptMessageHandler {
    weak var scriptDelegate: WKScriptMessageHandler?

    init(_ scriptDelegate: WKScriptMessageHandler) {
        self.scriptDelegate = scriptDelegate
        super.init()
    }

    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        print("js message: ", message.body)
    }
}

```

## Multithread
```swift
struct New: Codable{

}
JSONDecode(); // 解码返回的数据格式
```

js的json对象（Javascript object notation）swift没有

字典和结构体二选一
```swift
let dict: [String: String] = ["name": "Yoga", "title": "Developer"]
dict["title"]

struct Developer {
  var name: String
  var title: String
  init(_ name: String, _ title: String) {
    self.name = name
    self.title = title
  }
}

let yoga = Developer.init("Yoga", "Developer");
yoga.title
```

Alamofire

Moya

SwiftyJson