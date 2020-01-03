export const convertXYToObj = (x, y) => {
    const ret = {}
    x.forEach((x, idx) => {
        ret[String(x)] = y[idx]
    })
    return ret
}

export const groupPartitionedData = data => {
    const groupedData = {}
    const keys = Object.keys(data[0])
    keys.forEach(k => groupedData[k] = data.map(obj => obj[k]))
    groupedData.total = data.map(obj => Object.values(obj).reduce((acc, val) => acc + val))
    return groupedData
}