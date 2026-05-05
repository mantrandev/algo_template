// swift-tools-version: 6.3
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "algo_template",
    targets: [
        .executableTarget(
            name: "algo_template"
        ),
        .testTarget(
            name: "algo_templateTests",
            dependencies: ["algo_template"]
        ),
    ],
    swiftLanguageModes: [.v6]
)
