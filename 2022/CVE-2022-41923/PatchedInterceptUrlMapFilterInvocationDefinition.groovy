package demo

import grails.plugin.springsecurity.web.access.intercept.InterceptUrlMapFilterInvocationDefinition
import org.springframework.web.util.UrlPathHelper

import javax.servlet.http.HttpServletRequest

class PatchedInterceptUrlMapFilterInvocationDefinition extends InterceptUrlMapFilterInvocationDefinition {

    private static final UrlPathHelper urlPathHelper = new UrlPathHelper()

    @Override
    protected String calculateUri(HttpServletRequest request) {
        String requestUri = urlPathHelper.getRequestUri(request)
        stripContextPath(requestUri, request)
    }

    protected String stripContextPath(String uri, HttpServletRequest request) {
        String contextPath = request.contextPath
        if (contextPath && uri.startsWith(contextPath)) {
            uri = uri.substring(contextPath.length())
        }
        uri
    }

}
