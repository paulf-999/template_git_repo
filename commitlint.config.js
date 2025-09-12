module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
        // Only allow these types
        'type-enum': [
            2,
            'always',
            ['feat', 'fix', 'chore', 'docs', 'refactor', 'test', 'perf']
        ],
        // Scope is optional (don’t error if it’s missing)
        'scope-empty': [0],
        // Don’t nitpick subject casing/punctuation; keeps errors focused on the prefix
        'subject-case': [0],
        'subject-full-stop': [0],
        // Reasonable header length
        'header-max-length': [2, 'always', 100],
    }
};
