<div class="post-content">
  <h2 id="servicenow-insecure-access-control-leading-to-administrator-account-takeover---cve-2022-43684"><span class="mr-2">ServiceNow Insecure Access Control leading to Administrator Account Takeover - <strong>CVE-2022-43684</strong></span><a href="#servicenow-insecure-access-control-leading-to-administrator-account-takeover---cve-2022-43684" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>In this article, we will discuss a series of vulnerabilities that when exploited in succession, could enable a low-privilege user in ServiceNow to gain unauthorized full administrative access to the ServiceNow instance.</p>

<p>ServiceNow is a cloud-based platform that provides service management software as a service (SaaS). It is used by a millions of companies worldwide, and specializes in IT Service Management (ITSM), IT Operations Management (ITOM), and IT Business Management (ITBM). It allows users to manage incidents, service requests, problems, and changes within the IT infrastructure of a business. It also provides a self-service portal where end users can request IT services and log issues.</p>

<p>While working internally as a security engineer on the offensive security team, we routinely scrutinize the security of third-party platforms that integrate with our systems and processes. This is a crucial step to verify the security of these platforms and prevent potential breaches that could expose our sensitive data. During a recent engagement in mid-2022 our security team was able to exploit a number of vulnerabilities in ServiceNow leading to an effective account takeover to obtain administrative access on the platform as a low privileged user.</p>

<h2 id="table-of-contents"><span class="mr-2">Table of Contents</span><a href="#table-of-contents" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>
<ul>
  <li>Exploring the ServiceNow application</li>
  <li>Discovering the XHR request behind ‘Interactive Analysis’</li>
  <li>Enumerating tables using Glide Query Language (GQL)</li>
  <li>Constructing a valid session to escalate privileges to Administrator</li>
  <li>Ending Statement</li>
  <li>Credits</li>
  <li>Disclosure Timeline</li>
</ul>

<h2 id="exploring-the-servicenow-application"><span class="mr-2">Exploring the ServiceNow application</span><a href="#exploring-the-servicenow-application" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>While exploring the ServiceNow application, we determined that the application uses <code class="language-plaintext highlighter-rouge">.do</code> pages. <code class="language-plaintext highlighter-rouge">.do</code> endpoints are often associated with Java servlets, which are used to process requests and return dynamic content. As these pages query server-side resources, it should be secured against unauthorized or unintended access to prevent users from gaining access to sensitive functionality.</p>

<p>ServiceNow also uses Xml Http Requests (XHR), which is a fundamental technology behind Asynchronous JavaScript and XML (AJAX). The use of these API calls are to allow the performance of various operations without needing a full refresh of the page, which can improve the usability and efficiency of the application. ServiceNow widely uses XHR requests to update records or interacting with certain server-side resources or ‘processors’.</p>

<p>The application also uses the Glide Query Language (GQL), which is an proprietary, object-oriented language that forms the basis for the ServiceNow API to perform CRUD operations on its database. In essence, GQL serves as an abstraction layer for SQL operations that allows developers to perform database operations without interacting with raw SQL.</p>

<p>As a low privilege user, we discovered that it was not possible to directly access many of the application’s functionalities. An example is shown below, where we attempted to view the <code class="language-plaintext highlighter-rouge">$interactive_analysis.do</code> page:</p>

<p><a href="https://x64.sh/assets/images/ServiceNow_Images/interactive_do.png" title="" class="popup img-link"><img width="872" alt="image" data-src="https://x64.sh/assets/images/ServiceNow_Images/interactive_do.png" data-proofer-ignore="" src="https://x64.sh/assets/images/ServiceNow_Images/interactive_do.png" data-loaded="true"></a></p>

<p>However, while navigating through the application, there are some locations that inadventently redirect us to sensitive pages by appending query strings needed to create a valid request. Due to insufficient access control being implemented, we discovered that a standard user could access the <code class="language-plaintext highlighter-rouge">$interactive_analysis.do</code> endpoint if the query string was correctly formatted. We can send the following request to successfully access the <code class="language-plaintext highlighter-rouge">$interactive_analysis.do</code> page:</p>

<pre><code class="language-HTML">https://somehost.service-now.com/$interactive_analysis.do?sysparm_field=password&amp;sysparm_table=sys_user&amp;sysparm_from_list=true&amp;sysparm_query=active%3Dtrue%5Ecaller_id%3Djavascript:gs.getUserID()&amp;sysparm_list_view=&amp;sysparm_tiny_url=f040a8971ba38150d88b624c274bcbb3  
</code></pre>

<p>This is shown below:</p>

<p><a href="https://x64.sh/assets/images/ServiceNow_Images/chart_do.png" title="" class="popup img-link"><img width="967" alt="image" data-src="https://x64.sh/assets/images/ServiceNow_Images/chart_do.png" data-proofer-ignore="" src="https://x64.sh/assets/images/ServiceNow_Images/chart_do.png" data-loaded="true"></a></p>

<p>This is a very interesting functionality, because at first glance it provides the low privilege user with a graphical representation of all the users that are within the application, which could potentially signal that potentially sensitive information is being retrieved through some database.</p>

<h2 id="discovering-the-xhr-request-behind-interactive-analysis"><span class="mr-2">Discovering the XHR request behind ‘Interactive Analysis</span><a href="#discovering-the-xhr-request-behind-interactive-analysis" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>Through further investigation, we determined that the <code class="language-plaintext highlighter-rouge">$interactive_analysis.do</code> page, as well as the corresponding <code class="language-plaintext highlighter-rouge">report_viewer.do</code> (by accessing the chart from a separate page), sends an XHR request to <code class="language-plaintext highlighter-rouge">xmlhttp.do</code> with the “ChartDataProcessor” processor in the POST request. The initial output is quite complex, however it is possible to decode/trim the request and simplify it to the following POST body:</p>

<div class="language-plaintext highlighter-rouge"><div class="code-header">
        <span data-label-text="Plaintext"><i class="fas fa-code small"></i></span>
      <button aria-label="copy" data-title-succeed="Copied!" data-original-title="" title=""><i class="far fa-clipboard"></i></button></div><div class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">1
</pre></td><td class="rouge-code"><pre>sysparm_request_params={"page_num":"0","series":[{"table":"sys_user","groupby":"name","filter":"","plot_type":"horizontal_bar"}]}&amp;sysparm_processor=ChartDataProcessor 
</pre></td></tr></tbody></table></code></div></div>

<h2 id="enumerating-tables-using-glide-query-language-gql"><span class="mr-2">Enumerating tables using Glide Query Language (GQL)</span><a href="#enumerating-tables-using-glide-query-language-gql" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>We identified that ServiceNow sent an XHR request to <code class="language-plaintext highlighter-rouge">xmlhttp.do</code> with the “ChartDataProcessor” processor in a GQL format. As previously mentioned, Glide Query Language is a language that is specifically used for ServiceNow, and the processors were scripts that run server-side that can be called through the XHR request. It is similar to SQL in the format structure sent in the POST request.</p>

<p>We identifed that the following parameters are of interest:</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">table</code>: The specific database table used by the application.</li>
  <li><code class="language-plaintext highlighter-rouge">groupby</code>: Retrieves the rows from the specified column. This only retrieves the first 10 values used for rendering the chart/graph, however we can modify the “page_num” to enumerate all the values.</li>
  <li><code class="language-plaintext highlighter-rouge">filter</code>: Filtering the results retrieved from the GQL query.</li>
</ul>

<p>Leveraging this access control issue we enumerated a number of databases using Burp Suite Intruder and online documentation used by developers of ServiceNow third party plugins. This section of the test required a lot of trial and error to identify potentially useful tables, as there were hundreds of different tables containing varying degrees of sensitive data. We identified that the following tables were particularly interesting for a threat actor:</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">sys_db_object</code>: Retrieves the complete list of tables used by the application.</li>
  <li><code class="language-plaintext highlighter-rouge">sys_user</code>: List of all users</li>
  <li><code class="language-plaintext highlighter-rouge">sys_emails</code>: List of all emails</li>
</ul>

<p>According to the documentation, to be able to view ServiceNow tables we need to have read access to at least the ServiceNow tables <code class="language-plaintext highlighter-rouge">sys_db_object</code>, <code class="language-plaintext highlighter-rouge">sys_dictionary</code>, and <code class="language-plaintext highlighter-rouge">sys_glide_object</code>, and in addition to that to the tables you want to view, including referenced tables. However we were not allowed to access certain fields such as the <code class="language-plaintext highlighter-rouge">user_password</code> column in the <code class="language-plaintext highlighter-rouge">sys_user</code> table, as this would be an easy method to obtain privilege escalation against the system. Through further enumeration however, we were able to find two additional interesting tables, which will prove to be extremely useful later on:</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">sys_user_session</code>: Retrieves the “glide_session_store” and “X-Usertoken” used by any account.</li>
  <li><code class="language-plaintext highlighter-rouge">sys_user_token</code>: Partially retrieves the “glide_user_activity” value.</li>
</ul>

<h2 id="constructing-a-valid-session-to-escalate-privileges-to-administrator"><span class="mr-2">Constructing a valid session to escalate privileges to Administrator</span><a href="#constructing-a-valid-session-to-escalate-privileges-to-administrator" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>When testing the application and enumerating the database using the GQL language, we also noted that a valid authenticated session requires the following cookies/headers:</p>

<ul>
  <li>First method: The <code class="language-plaintext highlighter-rouge">glide_user_activity</code> and <code class="language-plaintext highlighter-rouge">glide_session_store</code> cookies, and the <code class="language-plaintext highlighter-rouge">X-Usertoken</code> header to be correctly set, OR</li>
  <li>Second method: The <code class="language-plaintext highlighter-rouge">JSESSIONID</code> cookie and the <code class="language-plaintext highlighter-rouge">X-Usertoken</code> header to be correctly set.</li>
</ul>

<p>As it was possible to leak the tables we assumed that <code class="language-plaintext highlighter-rouge">sys_user_session</code> and <code class="language-plaintext highlighter-rouge">sys_user_token</code> would be all we needed to steal other accounts. While this was true there proved to be more nuance that made it more difficult to exploit.</p>

<p>The second method initially stood out since the knowledge of a <code class="language-plaintext highlighter-rouge">JSESSIONID</code> cookie and the <code class="language-plaintext highlighter-rouge">X-Usertoken</code> header would lead to an effective account takeover of any logged in administator user. Ultimately, we were unable to obtain the <code class="language-plaintext highlighter-rouge">JSESSIONID</code> from any table, however it may be possible to leverage XSS/CSRF for a successful account takeover, but this was never attempted because we were able to retrieve a valid pathway to exploitation using the first method. The steps are outlined as follows:</p>

<p>Firstly, we can use the following query to retrieve the <code class="language-plaintext highlighter-rouge">glide_session_store</code>, which is used to store session information for users. Each record represents a unique session for each user, as well as other related information:</p>

<div class="language-plaintext highlighter-rouge"><div class="code-header">
        <span data-label-text="Plaintext"><i class="fas fa-code small"></i></span>
      <button aria-label="copy" data-title-succeed="Copied!" data-original-title="" title=""><i class="far fa-clipboard"></i></button></div><div class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">1
</pre></td><td class="rouge-code"><pre>sysparm_request_params={"page_num":"0","series":[{"table":"sys_user_session","groupby":"id","filter":"nameCONTAINS[Insert_Admin_Email_Here]^invalidatedISNULL","plot_type":"horizontal_bar"}]}&amp;sysparm_processor=ChartDataProcessor 
</pre></td></tr></tbody></table></code></div></div>

<p>Note that the results are filtered by the name of the target user, which we can enumerate using the <code class="language-plaintext highlighter-rouge">sys_user</code> table - this can also help us determine who the administrators of the instance are. The <code class="language-plaintext highlighter-rouge">^invalidatedISNULL</code> removes all the invalidated or expired tokens.</p>

<p>Secondly, we need to retrieve the <code class="language-plaintext highlighter-rouge">X-Usertoken</code> value from the <code class="language-plaintext highlighter-rouge">sys_user_session</code> table, which is the CSRF token that the application provides users to ensure that requests made are genuine and not malicious. We require this token to make subsequent requests to the server.</p>

<div class="language-plaintext highlighter-rouge"><div class="code-header">
        <span data-label-text="Plaintext"><i class="fas fa-code small"></i></span>
      <button aria-label="copy" data-title-succeed="Copied!" data-original-title="" title=""><i class="far fa-clipboard"></i></button></div><div class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">1
</pre></td><td class="rouge-code"><pre>sysparm_request_params={"page_num":"0","series":[{"table":"sys_user_session","groupby":"csrf_token","filter":"nameCONTAINS[Insert_Admin_Email_Here]^invalidatedISNULL","plot_type":"horizontal_bar"}]}&amp;sysparm_processor=ChartDataProcessor 
</pre></td></tr></tbody></table></code></div></div>

<p>The most difficult aspect was to determine a valid <code class="language-plaintext highlighter-rouge">glide_user_activity</code> token. A standard <code class="language-plaintext highlighter-rouge">glide_user_activity</code> token looks like this:</p>

<div class="language-plaintext highlighter-rouge"><div class="code-header">
        <span data-label-text="Plaintext"><i class="fas fa-code small"></i></span>
      <button aria-label="copy" data-title-succeed="Copied!" data-original-title="" title=""><i class="far fa-clipboard"></i></button></div><div class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">1
</pre></td><td class="rouge-code"><pre>U0N2M18xOmV4VFozT2Eyb2p0OVVWcXY5WktIeUl2L2h5MjFBMlY1d3RnRWkrUVpkZnM9Ok9NNzFIRDV1S0ZBMy90L1plMW5oQXk0OWliYVdBMXFlZUc5cmE3aGdPQ1E9
</pre></td></tr></tbody></table></code></div></div>

<p>We can make the following request to retrieve the partial token from the database:</p>

<div class="language-plaintext highlighter-rouge"><div class="code-header">
        <span data-label-text="Plaintext"><i class="fas fa-code small"></i></span>
      <button aria-label="copy" data-title-succeed="Copied!" data-original-title="" title=""><i class="far fa-clipboard"></i></button></div><div class="highlight"><code><table class="rouge-table"><tbody><tr><td class="rouge-gutter gl"><pre class="lineno">1
</pre></td><td class="rouge-code"><pre>sysparm_request_params={"page_num":"0","series":[{"table":"sys_user_token","groupby":"token","filter":"nameCONTAINS[Insert_Admin_Email_Here]","plot_type":"horizontal_bar"}]}&amp;sysparm_processor=ChartDataProcessor 
</pre></td></tr></tbody></table></code></div></div>

<p>However the values that were retrieved from <code class="language-plaintext highlighter-rouge">sys_user_token</code> appeared as follows:</p>

<p><a href="https://x64.sh/assets/images/ServiceNow_Images/jwt_error.png" title="" class="popup img-link"><img width="967" alt="image" data-src="https://x64.sh/assets/images/ServiceNow_Images/jwt_error.png" data-proofer-ignore="" src="https://x64.sh/assets/images/ServiceNow_Images/jwt_error.png" data-loaded="true"></a></p>

<p>Each <code class="language-plaintext highlighter-rouge">glide_user_activity</code> token could be base64 decoded however, revealing that the value from <code class="language-plaintext highlighter-rouge">sys_user_token</code> was the first half of the token:</p>

<p><a href="https://x64.sh/assets/images/ServiceNow_Images/jwt_decode.png" title="" class="popup img-link"><img width="967" alt="image" data-src="https://x64.sh/assets/images/ServiceNow_Images/jwt_decode.png" data-proofer-ignore="" src="https://x64.sh/assets/images/ServiceNow_Images/jwt_decode.png" data-loaded="true"></a></p>

<p>Through trial and error, we determined that the signature section of the token was not sufficiently validated when sent to the server, and it was possible to simply replace or remove the second half of the token to create a valid token.</p>

<p>With all three requirements satisfied, it was then possible to takeover any account including administrative accounts with an active session on the ServiceNow instance. ServiceNow also implements impersonation to allow admin to login into any user account for debugging purposes, we were able to use the admin account to impersonate a spefical user admin account and grant our account admin privileges on the ServiceNow instance.</p>

<h2 id="ending-statement"><span class="mr-2">Ending Statement</span><a href="#ending-statement" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>Overall, we were able to leverage several vulnerabilities to escalate privileges from a standard user account to administrator of the ServiceNow instance. The following vulnerabilities allowed us to gain effective account takeover:</p>
<ul>
  <li>Insecure access control in the “ChartDataProcessor” processor</li>
  <li>Overly permissive read access to sensitive tables in ServiceNow database</li>
  <li>Insufficient signature validation of the <code class="language-plaintext highlighter-rouge">glide_user_activity</code> token</li>
</ul>

<p>While the root cause of the issue was due to a insecure access control, the other vulnerabilties discovered and chained together took a medium impact bug to a critical impact bug with a CVSS score of <em><code class="language-plaintext highlighter-rouge">9.9 - https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator?vector=AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H&amp;version=3.1</code></em></p>

<h2 id="credits"><span class="mr-2">Credits</span><a href="#credits" class="anchor text-muted"><i class="fas fa-hashtag"></i></a></h2>

<p>The multiple vulnerabilities leading to full compromise of the ServiceNow instance were discovered by Luke Symons, Tony Wu, Eldar Marcussen, Gareth Phillips, Jeff Thomas, Nadeem Salim, and Stephen Bradshaw.</p>
</div>
