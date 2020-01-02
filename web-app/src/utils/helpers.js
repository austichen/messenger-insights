export const convertXYToObj = (x, y) => {
    const ret = {}
    x.forEach((x, idx) => {
      ret[String(x)] = y[idx]
    })
    return ret
}
  