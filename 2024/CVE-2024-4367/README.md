# cve-2024-4367-PoC-fixed
PDF.js是由Mozilla维护的基于JavaScript的PDF查看器。此漏洞允许攻击者在打开恶意 PDF 文件后立即执行任意 JavaScript 代码。这会影响所有 Firefox 用户 （&lt;126），因为 Firefox 使用 PDF.js 来显示 PDF 文件，但也严重影响了许多基于 Web 和 Electron 的应用程序，这些应用程序（间接）使用 PDF.js 进行预览功能。
