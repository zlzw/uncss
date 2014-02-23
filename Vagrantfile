Vagrant.configure("2") do |config|
    config.vm.box = "saucy64"

    config.vbguest.auto_update = true

    config.vm.hostname = "uncss.local"

    config.hostsupdater.aliases = ["uncss.local"]

    config.vm.network :private_network, ip: "192.168.33.10"

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "ansible/playbook-vagrant.yml"
        ansible.inventory_path = "ansible/host_vagrant"
        ansible.host_key_checking = false
        ansible.verbose = "v"
    end
end
