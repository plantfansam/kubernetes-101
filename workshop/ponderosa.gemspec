# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "ponderosa"
  spec.version       = "0.1.0"
  spec.authors       = ["Sam Handler"]
  spec.email         = ["sam@ponderosa.io"]

  spec.summary       = "Jekyll theme for Ponderosa courses"
  spec.homepage      = "https://github.com/ponderosa-io/ponderosa-jekyll"

  spec.files         = `git ls-files -z`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_sass|LICENSE|README)!i) }

  spec.add_runtime_dependency "jekyll", "~> 3.8"
  spec.add_runtime_dependency "jekyll-paginate-v2", "~> 1.9.4"
  spec.add_runtime_dependency "jekyll-assets", "~> 3.0.12"

  spec.add_development_dependency "bundler", "~> 2.0.1"
  spec.add_development_dependency "rake", "~> 12.0"
end
