class VersionControl {
    private let bad: Int
    init(bad: Int) { self.bad = bad }
    func isBadVersion(_ version: Int) -> Bool { version >= bad }
}
