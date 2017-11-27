import pytest
from curequests import post
from curio.file import aopen

from utils import run_with_curio

TEST_DATA = 'test data\n'


@run_with_curio
async def test_upload_file(httpbin_both):
    files = {'file': open('tests/upload.txt', 'rb')}
    r = await post(httpbin_both + '/post', files=files)
    assert r.ok
    assert r.json()['files']['file'] == TEST_DATA


@pytest.mark.skip('TODO: curio.aopen has some issues')
@run_with_curio
async def test_upload_asyncfile(httpbin_both):
    files = {'file': aopen('tests/upload.txt', 'rb')}
    r = await post(httpbin_both + '/post', files=files)
    assert r.ok
    assert r.json()['files']['file'] == TEST_DATA


@run_with_curio
async def test_upload_headers(httpbin_both):
    f = ('upload.txt', open('tests/upload.txt', 'rb'), 'text/plain')
    files = {'file': f}
    r = await post(httpbin_both + '/post', files=files)
    assert r.ok
    assert r.json()['files']['file'] == TEST_DATA


@run_with_curio
async def test_upload_string(httpbin_both):
    f = ('upload.txt', TEST_DATA)
    files = {'file': f}
    r = await post(httpbin_both + '/post', files=files)
    assert r.ok
    assert r.json()['files']['file'] == TEST_DATA


@pytest.mark.skip('the server not support chunked request')
@run_with_curio
async def test_chunked_request(httpbin_both):
    def gen():
        yield b'hi'
        yield b'there'
    r = await post(httpbin_both + '/post', data=gen())
    assert r.ok


@run_with_curio
async def test_stream_upload(httpbin_both):
    with open('tests/upload.txt', 'rb') as f:
        r = await post(httpbin_both + '/post', data=f)
    assert r.ok
    assert r.json()['data'] == TEST_DATA