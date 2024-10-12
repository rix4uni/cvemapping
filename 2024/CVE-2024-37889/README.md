# CVE-2024-37889

CVE-2024-37889 is an Insecure Direct Object Reference vulnerability in a financial management application. This vulnerability allows any authenticated user of the system to view any invoice in the system by manipulating direct references in the URL.

# Analysis

While there is authorization checks in order to edit the invoice as seen here:
https://github.com/TreyWW/MyFinances/blob/372b15978b4b8cb050bf17ea610ec0fcc54f1672/backend/api/invoices/edit.py#L20
```def edit_invoice(request: HtmxHttpRequest):
    try:
        invoice = Invoice.objects.get(id=request.POST.get("invoice_id", ""))
    except Invoice.DoesNotExist:
        return JsonResponse({"message": "Invoice not found"}, status=404)

    if request.user.logged_in_as_team and request.user.logged_in_as_team != invoice.organization:
        return JsonResponse(
            {"message": "You do not have permission to edit this invoice"},
            status=403,
        )
    elif request.user != invoice.user:
        return JsonResponse(
            {"message": "You do not have permission to edit this invoice"},
            status=403,
        )
```

The pre-edit view is loaded without such checks as seen here:
https://github.com/TreyWW/MyFinances/blob/a5e363c290328ea7ee8b107627163eb909094993/backend/views/core/invoices/edit.py#L56
```def invoice_edit_page_get(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return JsonResponse({"message": "Invoice not found"}, status=404)

    # use to populate fields with existing data in edit_from_destination.html AND edit_to_destination.html
    data_to_populate = invoice_get_existing_data(invoice)
    return render(request, "pages/invoices/edit/edit.html", data_to_populate)
```

# Mitigation

The following code change remediated this vulnerability, however, had best practices been followed from the beginning this vulnerability would have been less severe.

```# gets invoice object from invoice id, convert obj to dict, and renders edit.html while passing the stored invoice values to frontend
def invoice_edit_page_get(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)

        if not invoice.has_access(request.user):
            messages.error(request, "You are not permitted to edit this invoice")
            return redirect("invoices:dashboard")
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice not found")
        return redirect("invoices:dashboard")

    # use to populate fields with existing data in edit_from_destination.html AND edit_to_destination.html
    data_to_populate = invoice_get_existing_data(invoice)
    return render(request, "pages/invoices/edit/edit.html", data_to_populate)
```

# Conclusion

Vulnerabilities are an unavoidable part of software development but following best practices and having good code hygeine we can lesson their severity. Had the developer followed the reccomendations of the community and generated complex identifiers this finding would have been catagorized as a CVSS 3.1 instead of a 6.3.
