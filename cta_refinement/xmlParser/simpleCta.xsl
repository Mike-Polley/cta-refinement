<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 

<xsl:template match="/simpleCta.xml">
  <html>
  <body>
  <h2>Simple Cta</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>Name</th>
    </tr>
    <xsl:for-each select="location">
    <tr>
      <td><xsl:value-of select="name"/></td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:stylesheet>