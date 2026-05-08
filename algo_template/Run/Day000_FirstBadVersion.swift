private typealias Solution = Day000Solution

private final class BruteForce: VersionControl {
    func firstBadVersion(_ n: Int) -> Int {
        for i in 1...n { if isBadVersion(i) { return i } }
        return n
    }
}

enum Day000_FirstBadVersion {
    private struct Case {
        let n: Int
        let bad: Int
        let expected: Int
    }

    static func run() {
        let manual = Day000Cases.manual.map { Case(n: $0.n, bad: $0.bad, expected: $0.expected) }

        let stress: [Case] = (0..<100).map { _ in
            let n = Int.random(in: 1...1000)
            let bad = Int.random(in: 1...n)
            return Case(n: n, bad: bad, expected: BruteForce(bad: bad).firstBadVersion(n))
        }

        check(label: "Manual", cases: manual, silent: false)
        check(label: "Stress", cases: stress, silent: true)
    }

    private static func check(label: String, cases: [Case], silent: Bool) {
        var passed = 0
        print("--- \(label) (\(cases.count)) ---")
        for tc in cases {
            let result = Solution(bad: tc.bad).firstBadVersion(tc.n)
            if result == tc.expected {
                passed += 1
                if !silent { print("✅ n=\(tc.n), bad=\(tc.bad) → \(result)") }
            } else {
                print("❌ n=\(tc.n), bad=\(tc.bad) → got \(result), expected \(tc.expected)")
            }
        }
        print("Summary: \(passed)/\(cases.count) passed\n")
    }
}
