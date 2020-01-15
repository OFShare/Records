### install ruby

- install from Ruby Version Manager (RVM).

- `sudo apt-get purge ruby*`

- ```shell
  # First install RVM
  curl -sSL https://rvm.io/mpapis.asc | gpg --import -
  curl -sSL https://rvm.io/pkuczynski.asc | gpg --import -
  curl -sSL https://get.rvm.io | bash -s stable
  
  # Second install ruby from RVM
  rvm install ruby-2.6.3
  
  # activate ruby
  bash --login
  ```

### reference

- https://www.ruby-lang.org/en/
- https://rvm.io/