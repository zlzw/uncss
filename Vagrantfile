Vagrant.configure("2") do |config|
    config.vm.box = "https://cloud-images.ubuntu.com/vagrant/saucy/current/saucy-server-cloudimg-amd64-vagrant-disk1.box"

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
