final class Day000Solution: VersionControl {
    func firstBadVersion(_ n: Int) -> Int {
        return bisec(1, n)
    }

    private func bisec(_ l: Int, _ r: Int) -> Int {
        if l >= r { return l }
        let m = (l + r) / 2
        return isBadVersion(m) ? bisec(l, m) : bisec(m + 1, r)
    }
}
