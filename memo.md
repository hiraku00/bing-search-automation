
ContentView.swift
```swift
import SwiftUI
import UIKit

struct ContentView: View {
    @State private var capturedImage: UIImage? = nil
    @State private var isShowingCamera = false
    @State private var isShowingSearchResults = false
    @State private var searchResults: [SearchResult] = []
    @State private var isLoading = false

    private let googleAPIKey: String = {
        guard let key = ProcessInfo.processInfo.environment["GOOGLE_CLOUD_VISION_API_KEY"] else {
            fatalError("GOOGLE_CLOUD_VISION_API_KEY not found in environment variables")
        }
        return key
    }()

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                if let image = capturedImage {
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFit()
                        .frame(height: 300)
                        .cornerRadius(12)
                } else {
                    ZStack {
                        Color.gray.opacity(0.2)
                        Text("No Image")
                            .foregroundColor(.gray)
                    }
                    .frame(height: 300)
                    .cornerRadius(12)
                }

                Button(action: {
                    isShowingCamera = true
                }) {
                    HStack {
                        Image(systemName: "camera.fill")
                        Text("Take Photo")
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal)

                Button(action: {
                    if let image = capturedImage {
                        startSearch(image: image)
                    }
                }) {
                    HStack {
                        Image(systemName: "magnifyingglass")
                        Text("Search Similar Items")
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(capturedImage == nil ? Color.gray : Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal)
                .disabled(capturedImage == nil)

                Spacer()
            }
            .padding()
            .navigationTitle("Find Vintage")
            .sheet(isPresented: $isShowingCamera) {
                ImagePicker(image: $capturedImage)
            }
            .overlay(
                isLoading ? LoadingView() : nil
            )
        }
    }

    private func startSearch(image: UIImage) {
        isLoading = true
        searchSimilarImages(image: image) { results in
            isLoading = false
            searchResults = results
            print("🔍 検索結果: \(results)")  // ← 追加
            isShowingSearchResults = true
        }
    }

    private func searchSimilarImages(image: UIImage, completion: @escaping ([SearchResult]) -> Void) {
        guard let imageData = image.jpegData(compressionQuality: 0.8)?.base64EncodedString() else {
            completion([])
            return
        }

        let url = URL(string: "https://vision.googleapis.com/v1/images:annotate?key=\(googleAPIKey)")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let requestBody: [String: Any] = [
            "requests": [
                [
                    "image": ["content": imageData],
                    "features": [["type": "WEB_DETECTION"]]
                ]
            ]
        ]

        request.httpBody = try? JSONSerialization.data(withJSONObject: requestBody)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("❌ APIリクエストエラー: \(error.localizedDescription)")
                completion([])
                return
            }

            guard let data = data else {
                print("❌ APIからのデータが空")
                completion([])
                return
            }

            do {
                let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                print("📥 APIレスポンス: \(String(describing: json))")  // ← 追加
                let results = parseVisionResults(json: json)
                completion(results)
            } catch {
                print("❌ JSONパースエラー: \(error)")
                completion([])
            }
        }.resume()
    }

    private func parseVisionResults(json: [String: Any]?) -> [SearchResult] {
        guard let responses = json?["responses"] as? [[String: Any]],
              let webDetection = responses.first?["webDetection"] as? [String: Any],
              let visuallySimilarImages = webDetection["visuallySimilarImages"] as? [[String: Any]] else {
            return []
        }

        return visuallySimilarImages.compactMap { item in
            guard let url = item["url"] as? String else { return nil }
            return SearchResult(url: url)  // SearchResult.swift にある構造体を利用
        }
    }
}






//import SwiftUI
//import UIKit
//
//struct ContentView: View {
//    @State private var capturedImage: UIImage? = nil
//    @State private var isShowingCamera = false
//    @State private var isShowingSearchResults = false
//    @State private var searchResults: [SearchResult] = []
//    @State private var isLoading = false
//    @State private var errorMessage: String?
//
//    // 環境変数からAPIキーを取得
//    private let visionAPIKey: String = {
//        guard let key = ProcessInfo.processInfo.environment["GOOGLE_VISION_API_KEY"] else {
//            fatalError("GOOGLE_VISION_API_KEY not found in environment variables")
//        }
//        return key
//    }()
//
//    var body: some View {
//        NavigationView {
//            NavigationStack {
//                VStack(spacing: 20) {
//                    // プレビュー画像
//                    if let image = capturedImage {
//                        Image(uiImage: image)
//                            .resizable()
//                            .scaledToFit()
//                            .frame(height: 300)
//                            .cornerRadius(12)
//                    } else {
//                        ZStack {
//                            Color.gray.opacity(0.2)
//                            Text("No Image")
//                                .foregroundColor(.gray)
//                        }
//                        .frame(height: 300)
//                        .cornerRadius(12)
//                    }
//
//                    // カメラボタン
//                    Button(action: {
//                        isShowingCamera = true
//                    }) {
//                        HStack {
//                            Image(systemName: "camera.fill")
//                            Text("Take Photo")
//                        }
//                        .padding()
//                        .frame(maxWidth: .infinity)
//                        .background(Color.blue)
//                        .foregroundColor(.white)
//                        .cornerRadius(10)
//                    }
//                    .padding(.horizontal)
//
//                    // 検索ボタン
//                    Button(action: {
//                        if let image = capturedImage {
//                            startSearch(image: image)
//                        }
//                    }) {
//                        HStack {
//                            Image(systemName: "magnifyingglass")
//                            Text("Search Similar Items")
//                        }
//                        .padding()
//                        .frame(maxWidth: .infinity)
//                        .background(capturedImage == nil ? Color.gray : Color.green)
//                        .foregroundColor(.white)
//                        .cornerRadius(10)
//                    }
//                    .padding(.horizontal)
//                    .disabled(capturedImage == nil)
//
//                    Spacer()
//                }
//                .padding()
//                .navigationTitle("Find Vintage")
//                .sheet(isPresented: $isShowingCamera) {
//                    ImagePicker(image: $capturedImage)
//                }
//                .navigationDestination(isPresented: $isShowingSearchResults) {
//                    SearchResultsView(results: searchResults)
//                }
//                .overlay(
//                    isLoading ? LoadingView() : nil
//                )
//                .overlay(
//                    Group {
//                        if let error = errorMessage {
//                            ErrorAlertView(message: error)
//                        }
//                    }
//                )
//            }
//        }
//    }
//
//    // 検索開始
//    private func startSearch(image: UIImage) {
//        isLoading = true
//        errorMessage = nil
//
//        analyzeImageWithVision(image: image) { results in
//            isLoading = false
//            if results.isEmpty {
//                errorMessage = "類似画像が見つかりませんでした"
//            } else {
//                searchResults = results
//                isShowingSearchResults = true
//            }
//        }
//    }
//
//    // Vision APIを使用して画像を解析
//    private func analyzeImageWithVision(image: UIImage, completion: @escaping ([SearchResult]) -> Void) {
//        guard let imageData = image.jpegData(compressionQuality: 0.7) else {
//            completion([])
//            return
//        }
//
//        let requestBody: [String: Any] = [
//            "requests": [
//                [
//                    "image": ["content": imageData.base64EncodedString()],
//                    "features": [["type": "WEB_DETECTION"]]
//                ]
//            ]
//        ]
//
//        guard let url = URL(string: "https://vision.googleapis.com/v1/images:annotate?key=\(visionAPIKey)") else {
//            completion([])
//            return
//        }
//
//        var request = URLRequest(url: url)
//        request.httpMethod = "POST"
//        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
//
//        do {
//            request.httpBody = try JSONSerialization.data(withJSONObject: requestBody)
//        } catch {
//            completion([])
//            return
//        }
//
//        URLSession.shared.dataTask(with: request) { data, response, error in
//            DispatchQueue.main.async {
//                if let error = error {
//                    self.errorMessage = "通信エラー: \(error.localizedDescription)"
//                    completion([])
//                    return
//                }
//
//                guard let data = data else {
//                    self.errorMessage = "データがありません"
//                    completion([])
//                    return
//                }
//
//                let results = self.parseVisionResponse(data: data)
//                completion(results)
//            }
//        }.resume()
//    }
//
//    // Vision APIのレスポンスをパース
//    private func parseVisionResponse(data: Data) -> [SearchResult] {
//        do {
//            let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
//            guard let responses = json?["responses"] as? [[String: Any]],
//                  let webDetection = responses.first?["webDetection"] as? [String: Any] else {
//                return []
//            }
//
//            var results = [SearchResult]()
//
//            // 完全一致画像
//            if let fullMatches = webDetection["fullMatchingImages"] as? [[String: String]] {
//                results += fullMatches.compactMap { SearchResult(url: $0["url"] ?? "") }
//            }
//
//            // 部分一致画像
//            if let partialMatches = webDetection["partialMatchingImages"] as? [[String: String]] {
//                results += partialMatches.compactMap { SearchResult(url: $0["url"] ?? "") }
//            }
//
//            // 視覚的類似画像
//            if let similarImages = webDetection["visuallySimilarImages"] as? [[String: String]] {
//                results += similarImages.compactMap { SearchResult(url: $0["url"] ?? "") }
//            }
//
//            return results
//        } catch {
//            print("JSON Parsing Error: \(error)")
//            return []
//        }
//    }
//}
//





















//import SwiftUI
//import UIKit
//
//struct ContentView: View {
//    @State private var capturedImage: UIImage? = nil
//    @State private var isShowingCamera = false
//    @State private var isShowingSearchResults = false
//    @State private var searchResults: [SearchResult] = []
//    @State private var isLoading = false
//
//    // 環境変数からAPIキーと検索エンジンIDを取得
//    private let googleAPIKey: String = {
//        guard let key = ProcessInfo.processInfo.environment["GOOGLE_CUSTOM_SEARCH_API_KEY"] else {
//            fatalError("GOOGLE_CUSTOM_SEARCH_API_KEY not found in environment variables")
//        }
//        return key
//    }()
//
//    private let searchEngineID: String = {
//        guard let id = ProcessInfo.processInfo.environment["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"] else {
//            fatalError("GOOGLE_CUSTOM_SEARCH_ENGINE_ID not found in environment variables")
//        }
//        return id
//    }()
//
//    var body: some View {
//        NavigationView {
//            NavigationStack { // NavigationStack で囲む
//                VStack(spacing: 20) {
//                    // プレビュー画像
//                    if let image = capturedImage {
//                        Image(uiImage: image)
//                            .resizable()
//                            .scaledToFit()
//                            .frame(height: 300)
//                            .cornerRadius(12)
//                    } else {
//                        ZStack {
//                            Color.gray.opacity(0.2)
//                            Text("No Image")
//                                .foregroundColor(.gray)
//                        }
//                        .frame(height: 300)
//                        .cornerRadius(12)
//                    }
//
//                    // カメラボタン
//                    Button(action: {
//                        isShowingCamera = true
//                    }) {
//                        HStack {
//                            Image(systemName: "camera.fill")
//                            Text("Take Photo")
//                        }
//                        .padding()
//                        .frame(maxWidth: .infinity)
//                        .background(Color.blue)
//                        .foregroundColor(.white)
//                        .cornerRadius(10)
//                    }
//                    .padding(.horizontal)
//
//                    // 検索ボタン
//                    Button(action: {
//                        if let image = capturedImage {
//                            startSearch(image: image)
//                        }
//                    }) {
//                        HStack {
//                            Image(systemName: "magnifyingglass")
//                            Text("Search Similar Items")
//                        }
//                        .padding()
//                        .frame(maxWidth: .infinity)
//                        .background(capturedImage == nil ? Color.gray : Color.green)
//                        .foregroundColor(.white)
//                        .cornerRadius(10)
//                    }
//                    .padding(.horizontal)
//                    .disabled(capturedImage == nil)
//
//                    Spacer()
//                }
//                .padding()
//                .navigationTitle("Find Vintage")
//                .sheet(isPresented: $isShowingCamera) {
//                    ImagePicker(image: $capturedImage)
//                }
//                // NavigationLinkを削除し、navigationDestinationを使用
//                .navigationDestination(isPresented: $isShowingSearchResults) {
//                    SearchResultsView(results: searchResults)
//                }
//                .overlay(
//                    isLoading ? LoadingView() : nil
//                )
//            }
//        }
//    }
//
//    // 検索開始
//    private func startSearch(image: UIImage) {
//        isLoading = true
//        // Google Custom Search API を呼び出す
//        uploadImageToGoogleSearch(image: image) { results in
//            isLoading = false
//            searchResults = results
//            isShowingSearchResults = true
//        }
//    }
//
//    // Google Custom Search API への画像アップロード
//   private func uploadImageToGoogleSearch(image: UIImage, completion: @escaping ([SearchResult]) -> Void) {
//       guard let imageData = image.jpegData(compressionQuality: 0.8) else {
//           completion([])
//           return
//       }
//
//       let urlString = "https://www.googleapis.com/customsearch/v1"
//       var components = URLComponents(string: urlString)!
//       components.queryItems = [
//           URLQueryItem(name: "key", value: googleAPIKey),
//           URLQueryItem(name: "cx", value: searchEngineID),
//           URLQueryItem(name: "searchType", value: "image")
//       ]
//
//       guard let url = components.url else {
//           completion([])
//           return
//       }
//
//       var request = URLRequest(url: url)
//       request.httpMethod = "POST"
//       request.setValue("image/jpeg", forHTTPHeaderField: "Content-Type") // Content-Typeの設定
//
//       // APIリクエストのbodyに画像データを設定
//       request.httpBody = imageData
//
//       URLSession.shared.dataTask(with: request) { data, response, error in
//           if let error = error {
//               print("API Error: \(error)")
//               completion([])
//               return
//           }
//
//           // HTTPステータスコードの確認
//           if let httpResponse = response as? HTTPURLResponse {
//               if !(200...299).contains(httpResponse.statusCode) {
//                   print("HTTP Status Code: \(httpResponse.statusCode)")
//                   // エラーレスポンスの処理（例：エラーメッセージの出力）
//                   if let data = data, let errorMessage = String(data: data, encoding: .utf8) {
//                       print("Error Message from API: \(errorMessage)")
//                   }
//                   completion([])
//                   return
//               }
//           }
//
//           guard let data = data else {
//               completion([])
//               return
//           }
//
//           do {
//               // JSONのパース
//               let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
//               let results = self.parseSearchResults(json: json)
//               completion(results)
//           } catch {
//               print("JSON Parsing Error: \(error)")
//               // エラーの原因を特定するための情報をログに出力
//               if let jsonString = String(data: data, encoding: .utf8) {
//                   print("Received JSON String: \(jsonString)")
//               }
//               completion([])
//           }
//       }.resume()
//   }
//
//    // 検索結果のパース
//    private func parseSearchResults(json: [String: Any]?) -> [SearchResult] {
//        guard let items = json?["items"] as? [[String: Any]] else {
//            return []
//        }
//
//        return items.compactMap { item in
//            guard let title = item["title"] as? String,
//                  let link = item["link"] as? String else {
//                return nil
//            }
//            return SearchResult(title: title, link: link, confidence: 1.0)
//        }
//    }
//}
```

```swift
```

```swift
```

```swift
```
