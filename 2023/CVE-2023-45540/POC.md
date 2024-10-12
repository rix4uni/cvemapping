
>  Step To Reproduce:
>
>  	The following steps outline the exploitation of the HTML Injection vulnerability in Jorani Leave Management System v1.0.3         application:
>  
>  	    1. Launch the Jorani Leave Management System application.
>  
>  	    2. Open the Login page by accessing the URL: https://demo.jorani.org/session/login/ enter username and password.
>  
>  	    3. Click the Requests Button -> List of Leave requests -> view button 
>   
>  	    4. In Comments field <a href="https://static.wikia.nocookie.net/mrbean/images/4/4b/Mr_beans_holiday_ver2.jpg">HTML</a>
> 
>       5. Now able to Inject html injection in comments field 
> ------------------------------------------
>
> [Vulnerability Type]
> 
>   HTML Injection
>
> ------------------------------------------
>
> [Vendor of Product]
> 
>  https://jorani.org
>
> ------------------------------------------
>
> [Affected Product Code Base]
> 
>  Jorani Leave Management System v1.0.3 
>
> ------------------------------------------
>
> [Attack Type]
> 
>   Remote
>
> ------------------------------------------
>
> [Impact Code execution]
> 
>   true
>
> ------------------------------------------
>
> [Reference]
> 
>  https://jorani.org/download.html
> 
> ------------------------------------------
>
>[Discoverer]
> 
>   Soundar M
