export function chooseUploadFile() {
  return new Promise((resolve, reject) => {
    // #ifdef MP-WEIXIN
    uni.chooseMessageFile({
      count: 1,
      type: 'file',
      success: resolve,
      fail: reject
    })
    // #endif

    // #ifndef MP-WEIXIN
    uni.chooseFile({
      count: 1,
      type: 'all',
      extension: ['doc', 'docx', 'xls', 'xlsx', 'csv', 'txt', 'md'],
      success: resolve,
      fail: reject
    })
    // #endif
  })
}

export function normalizeChosenFile(res) {
  if (!res) return null
  if (res.tempFiles && res.tempFiles.length) {
    return res.tempFiles[0]
  }
  if (res.tempFilePaths && res.tempFilePaths.length) {
    return { path: res.tempFilePaths[0], name: 'upload' }
  }
  return null
}
