// swift-tools-version: 6.3
import PackageDescription

let package = Package(
    name: "algo_template",
    targets: [
        .executableTarget(
            name: "algo_template",
            path: ".",
            exclude: ["run.sh"]
        )
    ],
    swiftLanguageModes: [.v6]
)
